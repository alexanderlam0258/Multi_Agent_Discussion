import streamlit as st

from config.agents import AGENT_ROLES


def render_council_setup(
    available_models: dict[str, list[str]],
):

    st.header("🏛️ Council Setup")

    if not available_models:

        st.error(
            "No usable AI models are available."
        )

        return None

    providers = list(
        available_models.keys()
    )

    provider_display = {
        "gemini": "Gemini",
        "gpt": "OpenAI",
        "grok": "Grok",
        "deepseek": "DeepSeek",
        "openrouter": "OpenRouter",
    }

    def display_provider(provider: str):
        return provider_display.get(
            provider,
            provider.title(),
        )

    # -----------------------------------------------------
    # Chairman
    # -----------------------------------------------------

    st.subheader("👑 Chairman")

    chairman_provider = st.selectbox(
        "Chairman Provider",
        providers,
        format_func=display_provider,
        key="chairman_provider",
    )

    chairman_model = st.selectbox(
        "Chairman Model",
        available_models[chairman_provider],
        key="chairman_model",
    )

    chairman_characteristics = st.text_area(
        "Chairman Characteristics",
        value=(
            "Act as a neutral chairman. "
            "Integrate the discussion, identify agreements "
            "and disagreements, distinguish facts from "
            "interpretations, and produce a balanced synthesis."
        ),
        height=120,
        key="chairman_characteristics",
    )

    st.divider()

    # -----------------------------------------------------
    # Agents
    # -----------------------------------------------------

    st.subheader("🤖 Discussion Agents")

    agent_count = st.number_input(
        "Number of discussion agents",
        min_value=1,
        max_value=8,
        value=4,
        step=1,
    )

    role_names = list(
        AGENT_ROLES.keys()
    )

    agents = []

    for index in range(int(agent_count)):

        st.markdown(
            f"### Agent {index + 1}"
        )

        role = st.selectbox(
            "Role",
            role_names,
            key=f"agent_{index}_role",
        )

        role_config = AGENT_ROLES[role]

        st.caption(
            role_config.description
        )

        provider = st.selectbox(
            "Provider",
            providers,
            format_func=display_provider,
            key=f"agent_{index}_provider",
        )

        model = st.selectbox(
            "Model",
            available_models[provider],
            key=f"agent_{index}_model",
        )

        characteristics = st.text_area(
            "Characteristics",
            value=role_config.characteristics,
            height=100,
            key=f"agent_{index}_characteristics",
        )

        agents.append(
            {
                "name": f"Agent {index + 1}",
                "role": role,
                "provider": provider,
                "model": model,
                "characteristics": characteristics,
            }
        )

        st.divider()

    # -----------------------------------------------------
    # Start
    # -----------------------------------------------------

    start = st.button(
        "🚀 Start Discussion",
        type="primary",
        use_container_width=True,
    )

    if not start:
        return None

    return {
        "chairman": {
            "provider": chairman_provider,
            "model": chairman_model,
            "characteristics": chairman_characteristics,
        },
        "agents": agents,
    }