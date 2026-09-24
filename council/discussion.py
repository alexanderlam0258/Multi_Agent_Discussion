from openai import OpenAI


def run_agent_turn(
    client: OpenAI,
    model: str,
    agent_name: str,
    role_description: str,
    topic: str,
    background: str,
    rules: str,
    transcript: list[dict],
) -> str:

    system_prompt = f"""
You are participating in a multi-agent discussion.

Your role:
{agent_name}

Your role description:
{role_description}

TOPIC:
{topic}

BACKGROUND:
{background}

DISCUSSION RULES:
{rules}

You are one participant in a council.

You should:
- directly engage with previous arguments
- identify agreements and disagreements
- challenge weak reasoning
- introduce useful evidence or analysis
- avoid merely repeating previous statements
- advance the discussion
"""

    messages = [
        {
            "role": "system",
            "content": system_prompt.strip(),
        }
    ]

    for turn in transcript:

        speaker = turn.get(
            "speaker",
            "Unknown",
        )

        text = turn.get(
            "text",
            "",
        )

        messages.append(
            {
                "role": "user",
                "content": (
                    f"[{speaker}]:\n{text}"
                ),
            }
        )

    messages.append(
        {
            "role": "user",
            "content": (
                "It is your turn. "
                "Respond to the discussion and "
                "advance the analysis."
            ),
        }
    )

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7,
    )

    return (
        response.choices[0]
        .message
        .content
        or ""
    )


def run_chairman_synthesis(
    client: OpenAI,
    model: str,
    characteristics: str,
    topic: str,
    background: str,
    rules: str,
    transcript: list[dict],
) -> str:

    system_prompt = f"""
You are the Chairman of a multi-agent council.

Your characteristics:
{characteristics}

TOPIC:
{topic}

BACKGROUND:
{background}

DISCUSSION RULES:
{rules}

Your task is to synthesize the discussion.

Do not simply vote or count opinions.

Instead:
1. Identify the major areas of agreement.
2. Identify substantive disagreements.
3. Distinguish factual claims from interpretations.
4. Identify important assumptions.
5. Identify weaknesses or unresolved questions.
6. Present the strongest arguments from different sides.
7. Produce a clear final synthesis.

Do not invent evidence that was not discussed.
"""

    messages = [
        {
            "role": "system",
            "content": system_prompt.strip(),
        }
    ]

    for turn in transcript:

        speaker = turn.get(
            "speaker",
            "Unknown",
        )

        text = turn.get(
            "text",
            "",
        )

        messages.append(
            {
                "role": "user",
                "content": (
                    f"[{speaker}]:\n{text}"
                ),
            }
        )

    messages.append(
        {
            "role": "user",
            "content": (
                "As Chairman, provide the final synthesis "
                "of the council discussion."
            ),
        }
    )

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.4,
    )

    return (
        response.choices[0]
        .message
        .content
        or ""
    )