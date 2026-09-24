def build_agent_prompt(
    topic: str,
    background: str,
    rules: str,
    role_description: str,
) -> str:

    return f"""
You are participating in a multi-agent AI Council.

TOPIC:
{topic}

BACKGROUND:
{background}

GENERAL RULES:
{rules}

YOUR ROLE:
{role_description}

You must:
- reason independently;
- distinguish facts from assumptions;
- directly address relevant arguments;
- identify weaknesses where appropriate;
- add new analytical value;
- avoid agreeing merely to create consensus.
"""


def build_discussion_context(transcript: list) -> str:

    if not transcript:
        return "There are no previous statements."

    sections = []

    for turn in transcript:

        sections.append(
            f"--- {turn['agent']} "
            f"(Round {turn['round']}) ---\n"
            f"{turn['text']}"
        )

    return "\n\n".join(sections)