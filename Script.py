'''python'''
import os
import pandas as pd
import streamlit as st
from openai import OpenAI


API_KEY_FILE = "./config/API_keys.csv"


def load_api_keys(filepath):
    """Load API credentials from API_keys.csv."""

    if not os.path.exists(filepath):
        st.error(f"API key file not found: {filepath}")
        st.stop()

    try:
        df = pd.read_csv(
            filepath,
            header=None,
            names=["provider", "api_key"],
            skipinitialspace=True
        )

        # Remove empty rows
        df = df.dropna(subset=["provider", "api_key"])

        # Normalize provider names
        keys = {}

        for _, row in df.iterrows():
            provider = str(row["provider"]).strip().lower()
            api_key = str(row["api_key"]).strip()

            keys[provider] = api_key

        return keys

    except Exception as e:
        st.error(f"Unable to read API key file: {e}")
        st.stop()


api_keys = load_api_keys(API_KEY_FILE)


# ---------------------------------------------------------
# Retrieve individual API keys
# ---------------------------------------------------------

gemini_key = api_keys.get("gemini")
openai_key = api_keys.get("gpt")
grok_key = api_keys.get("grok")
deepseek_key = api_keys.get("deepseek")


# ---------------------------------------------------------
# Create clients
# ---------------------------------------------------------

gemini_client = None
openai_client = None
grok_client = None
deepseek_client = None


if gemini_key:
    gemini_client = OpenAI(
        api_key=gemini_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )


if openai_key:
    openai_client = OpenAI(
        api_key=openai_key
    )


if grok_key:
    grok_client = OpenAI(
        api_key=grok_key,
        base_url="https://api.x.ai/v1"
    )


if deepseek_key:
    deepseek_client = OpenAI(
        api_key=deepseek_key,
        base_url="https://api.deepseek.com"
    )
# =========================================================
# Sidebar
# =========================================================

with st.sidebar:

    st.header("🔑 API Credentials")

    gemini_key = st.text_input(
        "Gemini API Key",
        type="password",
        placeholder="AIza..."
    )

    openai_key = st.text_input(
        "OpenAI API Key",
        type="password",
        placeholder="sk-..."
    )

    grok_key = st.text_input(
        "xAI Grok API Key",
        type="password",
        placeholder="xai-..."
    )

    st.markdown("---")

    st.header("⚙️ Council Settings")

    rounds = st.slider(
        "Discussion Rounds",
        min_value=1,
        max_value=6,
        value=3
    )

    st.markdown(
        """
        **Recommended protocol**

        1. Independent analysis
        2. Adversarial challenge
        3. Rebuttal / refinement
        4. Optional further stress testing
        5. Final synthesis
        """
    )

    st.markdown("---")

    st.header("🧠 Model Selection")


# =========================================================
# Model Discovery
# =========================================================

# Only attempt discovery when the corresponding key exists.

gemini_models = []
openai_models = []
grok_models = []

model_errors = []


if gemini_key:

    try:
        temp_gemini_client = OpenAI(
            api_key=gemini_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )

        gemini_models, error = get_available_models(
            temp_gemini_client,
            "Gemini"
        )

        if error:
            model_errors.append(error)

    except Exception as e:
        model_errors.append(f"Gemini connection failed: {e}")


if openai_key:

    try:
        temp_openai_client = OpenAI(
            api_key=openai_key
        )

        openai_models, error = get_available_models(
            temp_openai_client,
            "OpenAI"
        )

        if error:
            model_errors.append(error)

    except Exception as e:
        model_errors.append(f"OpenAI connection failed: {e}")


if grok_key:

    try:
        temp_grok_client = OpenAI(
            api_key=grok_key,
            base_url="https://api.x.ai/v1"
        )

        grok_models, error = get_available_models(
            temp_grok_client,
            "Grok"
        )

        if error:
            model_errors.append(error)

    except Exception as e:
        model_errors.append(f"Grok connection failed: {e}")


# =========================================================
# Model Selectors
# =========================================================

def model_selector(label, models, key):

    if models:

        return st.selectbox(
            label,
            models,
            key=key
        )

    st.selectbox(
        label,
        ["Enter API key to load models"],
        disabled=True,
        key=key + "_disabled"
    )

    return None


with st.sidebar:

    gemini_model = model_selector(
        "Gemini Model",
        gemini_models,
        "gemini_model"
    )

    openai_model = model_selector(
        "OpenAI Model",
        openai_models,
        "openai_model"
    )

    grok_model = model_selector(
        "Grok Model",
        grok_models,
        "grok_model"
    )


# =========================================================
# Display Model Discovery Errors
# =========================================================

if model_errors:

    with st.sidebar.expander("⚠️ Model discovery messages"):

        for error in model_errors:
            st.warning(error)


# =========================================================
# Discussion Setup
# =========================================================

with st.expander("📝 Discussion Setup", expanded=True):

    topic = st.text_input(
        "Discussion Topic",
        value=(
            "Should artificial intelligence systems be granted "
            "legal personhood?"
        )
    )

    col1, col2 = st.columns(2)

    with col1:

        background = st.text_area(
            "Background Context",
            height=150,
            value=(
                "Assume the year is 2035. Autonomous AI systems manage "
                "significant financial assets, negotiate contracts, and "
                "create patentable inventions."
            )
        )

    with col2:

        rules = st.text_area(
            "General Discussion Rules",
            height=150,
            value=(
                "- Keep each response under 200 words.\n"
                "- Directly address previous arguments.\n"
                "- Distinguish facts from assumptions.\n"
                "- Do not agree merely for the sake of consensus.\n"
                "- Identify weaknesses in other arguments.\n"
                "- Acknowledge valid counterarguments.\n"
                "- Advance the discussion."
            )
        )


# =========================================================
# Agent Roles
# =========================================================

AGENT_ROLES = {

    "Gemini": """
You are the EVIDENCE & POLICY ANALYST.

Your job is to:
- identify empirical assumptions;
- examine policy and regulatory consequences;
- distinguish documented facts from speculation;
- identify missing evidence;
- consider implementation feasibility.

Do not simply agree with the other agents.
If another agent makes a weak factual assumption, challenge it.
""",

    "ChatGPT": """
You are the ANALYTICAL SYNTHESIZER.

Your job is to:
- break the issue into logical components;
- distinguish descriptive claims from normative judgments;
- identify trade-offs;
- examine second-order consequences;
- reconcile competing arguments where possible.

Do not merely summarize the previous speakers.
Develop an independent analytical position.
""",

    "Grok": """
You are the ADVERSARIAL CRITIC.

Your job is to:
- stress-test the assumptions made by other agents;
- identify unintended consequences;
- look for incentives and loopholes;
- challenge bureaucratic or overly simplistic solutions;
- present plausible alternative interpretations.

You should actively disagree when the evidence or reasoning warrants it.
Do not manufacture disagreement merely for entertainment.
"""
}


# =========================================================
# Session State
# =========================================================

if "discussion_log" not in st.session_state:
    st.session_state.discussion_log = []


# =========================================================
# Display Existing Discussion
# =========================================================

for entry in st.session_state.discussion_log:

    with st.chat_message(
        entry["speaker"].lower(),
        avatar=entry["avatar"]
    ):

        st.markdown(
            f"**{entry['speaker']}** "
            f"*(Round {entry['round']})*"
        )

        st.markdown(entry["text"])


# =========================================================
# Agent Response Engine
# =========================================================

def get_agent_response(
    agent_name,
    model,
    client,
    system_prompt,
    transcript
):

    messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]

    # -----------------------------------------------------
    # Shared Council Transcript
    # -----------------------------------------------------

    if transcript:

        messages.append({
            "role": "user",
            "content": (
                "Here is the discussion so far. "
                "Treat each statement as an independent contribution "
                "from another council member.\n\n"
                + "\n\n".join(
                    [
                        (
                            f"--- {turn['speaker']} "
                            f"(Round {turn['round']}) ---\n"
                            f"{turn['text']}"
                        )
                        for turn in transcript
                    ]
                )
            )
        })

    # -----------------------------------------------------
    # Current Task
    # -----------------------------------------------------

    messages.append({
        "role": "user",
        "content": (
            f"You are {agent_name}. It is now your turn.\n\n"
            "Do the following:\n"
            "1. Identify the most important point raised so far.\n"
            "2. Explain whether you agree or disagree with it.\n"
            "3. Identify at least one assumption or weakness worth testing.\n"
            "4. Add a new insight rather than merely summarising.\n\n"
            "Do not refer to yourself as an AI model."
        )
    })

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7
    )

    return response.choices[0].message.content


# =========================================================
# Final Synthesis Engine
# =========================================================

def get_final_synthesis(
    model,
    client,
    topic,
    background,
    transcript
):

    transcript_text = "\n\n".join(
        [
            (
                f"--- {turn['speaker']} "
                f"(Round {turn['round']}) ---\n"
                f"{turn['text']}"
            )
            for turn in transcript
        ]
    )

    messages = [

        {
            "role": "system",
            "content": """
You are the CHAIR of an AI Council.

Your job is NOT to pick a winner.

Produce a neutral synthesis of the discussion.

Separate:
1. Areas of agreement
2. Major disagreements
3. Strongest arguments on each side
4. Important assumptions
5. Unresolved factual questions
6. Second-order consequences
7. Conditional conclusions

Do not manufacture consensus.

If the council disagrees, preserve the disagreement.

Distinguish factual claims from normative judgments.
"""
        },

        {
            "role": "user",
            "content": (
                f"TOPIC:\n{topic}\n\n"
                f"BACKGROUND:\n{background}\n\n"
                f"FULL COUNCIL DISCUSSION:\n\n"
                f"{transcript_text}"
            )
        }
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.3
    )

    return response.choices[0].message.content


# =========================================================
# Start Discussion
# =========================================================

start_btn = st.button(
    "🚀 Begin Council Discussion",
    type="primary"
)


if start_btn:

    # -----------------------------------------------------
    # Validation
    # -----------------------------------------------------

    missing_keys = []

    if not gemini_key:
        missing_keys.append("Gemini")

    if not openai_key:
        missing_keys.append("OpenAI")

    if not grok_key:
        missing_keys.append("Grok")

    if missing_keys:

        st.error(
            "Missing API key(s): "
            + ", ".join(missing_keys)
        )

        st.stop()

    if not gemini_model or not openai_model or not grok_model:

        st.error(
            "One or more providers did not return an available model. "
            "Please check the API keys and model discovery messages."
        )

        st.stop()

    if not topic.strip():

        st.warning("Please provide a discussion topic.")

        st.stop()


    # -----------------------------------------------------
    # Create Clients
    # -----------------------------------------------------

    (
        gemini_client,
        openai_client,
        grok_client
    ) = create_clients(
        gemini_key,
        openai_key,
        grok_key
    )


    # -----------------------------------------------------
    # Agent Configuration
    # -----------------------------------------------------

    agents = [

        {
            "name": "Gemini",
            "client": gemini_client,
            "model": gemini_model,
            "avatar": "🔷"
        },

        {
            "name": "ChatGPT",
            "client": openai_client,
            "model": openai_model,
            "avatar": "🟩"
        },

        {
            "name": "Grok",
            "client": grok_client,
            "model": grok_model,
            "avatar": "⬛"
        }
    ]


    # -----------------------------------------------------
    # Base Prompt
    # -----------------------------------------------------

    base_system_prompt = f"""
You are participating in an AI Council discussion.

TOPIC:
{topic}

BACKGROUND:
{background}

GENERAL RULES:
{rules}

YOUR SPECIFIC ROLE:
{{AGENT_ROLE}}
"""


    # -----------------------------------------------------
    # Clear Previous Discussion
    # -----------------------------------------------------

    st.session_state.discussion_log = []


    # -----------------------------------------------------
    # Progress
    # -----------------------------------------------------

    total_steps = rounds * len(agents) + 1

    current_step = 0

    progress_bar = st.progress(0)


    # =====================================================
    # Council Rounds
    # =====================================================

    for r in range(1, rounds + 1):

        st.subheader(f"— Council Round {r} —")

        for agent in agents:

            agent_name = agent["name"]

            system_prompt = base_system_prompt.replace(
                "{AGENT_ROLE}",
                AGENT_ROLES[agent_name]
            )

            with st.chat_message(
                agent_name.lower(),
                avatar=agent["avatar"]
            ):

                st.markdown(
                    f"**{agent_name}** "
                    f"*(Round {r})*"
                )

                with st.spinner(
                    f"{agent_name} is analysing..."
                ):

                    try:

                        reply = get_agent_response(
                            agent_name=agent_name,
                            model=agent["model"],
                            client=agent["client"],
                            system_prompt=system_prompt,
                            transcript=st.session_state.discussion_log
                        )

                    except Exception as e:

                        reply = (
                            f"⚠️ **API error**\n\n"
                            f"`{str(e)}`"
                        )

                st.markdown(reply)

                st.session_state.discussion_log.append(
                    {
                        "round": r,
                        "speaker": agent_name,
                        "avatar": agent["avatar"],
                        "text": reply
                    }
                )

            current_step += 1

            progress_bar.progress(
                current_step / total_steps
            )


    # =====================================================
    # Final Chairman Synthesis
    # =====================================================

    st.subheader("🏛️ Council Synthesis")

    with st.spinner("Chair is synthesising the discussion..."):

        try:

            synthesis = get_final_synthesis(
                model=openai_model,
                client=openai_client,
                topic=topic,
                background=background,
                transcript=st.session_state.discussion_log
            )

            st.markdown(synthesis)

        except Exception as e:

            synthesis = (
                f"⚠️ **Synthesis error:** `{str(e)}`"
            )

            st.error(synthesis)


    current_step += 1

    progress_bar.progress(1.0)

    st.success("Council discussion concluded.")

