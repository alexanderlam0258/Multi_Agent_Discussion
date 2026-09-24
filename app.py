import streamlit as st

from config.api_keys import load_api_keys
from providers.clients import create_clients
from providers.models import discover_all_models

from ui.sidebar import render_sidebar
from ui.setup import render_council_setup

from council.discussion import (
    run_agent_turn,
    run_chairman_synthesis,
)


# =========================================================
# Page Configuration
# =========================================================

st.set_page_config(
    page_title="AI Council",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 AI Council")
st.caption(
    "Multi-agent discussion and collaborative reasoning"
)


# =========================================================
# Session State
# =========================================================

if "discussion_log" not in st.session_state:
    st.session_state.discussion_log = []

if "discussion_started" not in st.session_state:
    st.session_state.discussion_started = False


# =========================================================
# Load API Keys
# =========================================================

try:

    api_keys = load_api_keys()

except Exception as exc:

    st.error(
        f"Configuration error:\n\n{exc}"
    )

    st.stop()


if not api_keys:

    st.error(
        "No API keys were found in the API key file."
    )

    st.stop()


# =========================================================
# Create API Clients
# =========================================================

clients = create_clients(
    api_keys
)


if not clients:

    st.error(
        "No AI providers could be initialized."
    )

    st.stop()


# =========================================================
# Discover Models
# =========================================================

available_models, provider_errors = (
    discover_all_models(clients)
)


# =========================================================
# Provider Status
# =========================================================

with st.sidebar.expander(
    "🔌 Provider Status",
    expanded=True,
):

    for provider in clients:

        if provider in available_models:

            st.success(
                f"{provider.upper()} — "
                f"{len(available_models[provider])} models"
            )

        else:

            error = provider_errors.get(
                provider,
                "Unknown error",
            )

            st.error(
                f"{provider.upper()} unavailable\n\n"
                f"{error}"
            )


if not available_models:

    st.error(
        "No usable AI models are available."
    )

    st.stop()


# =========================================================
# Discussion Settings
# =========================================================

rounds = render_sidebar()


# =========================================================
# Discussion Brief
# =========================================================

st.header("📝 Discussion Brief")

topic = st.text_input(
    "Discussion Topic",
    value=(
        "Should artificial intelligence systems "
        "be granted legal personhood?"
    ),
    help="The central question that all agents will discuss.",
)

background = st.text_area(
    "Background Context",
    value=(
        "Assume the year is 2035. Autonomous AI systems "
        "manage significant financial assets, negotiate "
        "contracts and create patentable inventions."
    ),
    height=140,
    help=(
        "Provide facts, assumptions, scenarios or "
        "other context that all agents should know."
    ),
)

rules = st.text_area(
    "Discussion Rules",
    value=(
        "- Be concise.\n"
        "- Directly address previous arguments.\n"
        "- Challenge assumptions where appropriate.\n"
        "- Distinguish facts from interpretations.\n"
        "- Do not simply repeat previous arguments.\n"
        "- Advance the discussion."
    ),
    height=160,
    help=(
        "These rules apply to all discussion agents "
        "and the Chairman."
    ),
)


# =========================================================
# Council Setup
# =========================================================

setup_config = render_council_setup(
    available_models
)


if setup_config is None:

    st.info(
        "Configure the Chairman and discussion agents "
        "below, then click '🚀 Start Discussion'."
    )

    st.stop()



# =========================================================
# Start New Discussion
# =========================================================

st.session_state.discussion_log = []

st.session_state.discussion_started = True



# =========================================================
# Discussion Engine
# =========================================================

progress = st.progress(0)

agents = setup_config["agents"]

total_steps = (
    int(rounds) * len(agents)
)

current_step = 0


for round_number in range(
    1,
    int(rounds) + 1,
):

    st.subheader(
        f"— Round {round_number} —"
    )

    for agent in agents:

        provider = agent["provider"]
        model = agent["model"]
        role = agent["role"]
        characteristics = agent["characteristics"]

        # -------------------------------------------------
        # Defensive availability check
        # -------------------------------------------------

        if provider not in clients:

            st.warning(
                f"Skipping {role}: "
                f"{provider.upper()} is unavailable."
            )

            continue

        if provider not in available_models:

            st.warning(
                f"Skipping {role}: "
                f"{provider.upper()} has no usable models."
            )

            continue

        # -------------------------------------------------
        # Agent turn
        # -------------------------------------------------

        with st.chat_message(
            role.lower().replace(" ", "_")
        ):

            st.markdown(
                f"**{role}** "
                f"({provider.upper()} / {model})"
            )

            with st.spinner(
                f"{role} is thinking..."
            ):

                try:

                    response = run_agent_turn(
                        client=clients[provider],
                        model=model,
                        agent_name=role,
                        role_description=characteristics,
                        topic=topic,
                        background=background,
                        rules=rules,
                        transcript=(
                            st.session_state
                            .discussion_log
                        ),
                    )

                except Exception as exc:

                    st.error(
                        f"{provider.upper()} / {role} "
                        f"failed in Round "
                        f"{round_number}: "
                        f"{type(exc).__name__}: {exc}"
                    )

                    response = None

                if response:

                    st.markdown(response)

                    st.session_state.discussion_log.append(
                        {
                            "round": round_number,
                            "speaker": role,
                            "provider": provider,
                            "model": model,
                            "text": response,
                        }
                    )

        current_step += 1

        if total_steps > 0:

            progress.progress(
                current_step / total_steps
            )


# =========================================================
# Chairman
# =========================================================

st.divider()

st.subheader("👑 Chairman's Synthesis")

chairman = setup_config["chairman"]

chairman_provider = chairman["provider"]
chairman_model = chairman["model"]
chairman_characteristics = chairman[
    "characteristics"
]


if chairman_provider not in clients:

    st.error(
        "The selected Chairman provider is no longer available."
    )

    st.stop()


with st.spinner(
    "Chairman is reviewing the discussion..."
):

    try:

        final_response = run_chairman_synthesis(
            client=clients[chairman_provider],
            model=chairman_model,
            characteristics=chairman_characteristics,
            topic=topic,
            background=background,
            rules=rules,
            transcript=(
                st.session_state
                .discussion_log
            ),
        )

        st.markdown(final_response)

    except Exception as exc:

        st.error(
            f"Chairman failed: "
            f"{type(exc).__name__}: {exc}"
        )


st.success(
    "Discussion concluded."
)