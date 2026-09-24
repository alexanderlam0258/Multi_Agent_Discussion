from council.prompts import build_discussion_context


def run_synthesis(
    client,
    model: str,
    topic: str,
    background: str,
    transcript: list,
) -> str:

    context = build_discussion_context(transcript)

    system_prompt = """
You are the Chairman of an AI Council.

Produce a neutral synthesis.

Do not declare a winner.

Separate:

1. Areas of agreement
2. Major disagreements
3. Strong arguments on each side
4. Key assumptions
5. Unresolved factual questions
6. Second-order consequences
7. Conditional conclusions

Preserve genuine disagreement.
Do not manufacture consensus.
"""

    user_prompt = f"""
TOPIC:
{topic}

BACKGROUND:
{background}

COUNCIL DISCUSSION:
{context}

Produce the final council synthesis.
"""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        temperature=0.3,
    )

    content = response.choices[0].message.content

    if not content:
        raise RuntimeError(
            "Chairman returned an empty synthesis."
        )

    return content