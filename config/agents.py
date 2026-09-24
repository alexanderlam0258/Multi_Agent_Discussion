from dataclasses import dataclass


@dataclass(frozen=True)
class AgentRole:
    name: str
    description: str
    characteristics: str


AGENT_ROLES = {

    "Evidence Analyst": AgentRole(
        name="Evidence Analyst",
        description=(
            "Focuses on factual evidence, data, sources, "
            "assumptions and reliability of supporting information."
        ),
        characteristics=(
            "Evidence-driven, precise, quantitative, "
            "and careful about distinguishing facts from assumptions."
        ),
    ),

    "Analytical Lead": AgentRole(
        name="Analytical Lead",
        description=(
            "Develops the main analytical framework, "
            "connects evidence and produces coherent reasoning."
        ),
        characteristics=(
            "Structured, analytical, systematic and synthesis-oriented."
        ),
    ),

    "Adversarial Critic": AgentRole(
        name="Adversarial Critic",
        description=(
            "Actively challenges assumptions, reasoning and conclusions. "
            "Constructs credible counterarguments."
        ),
        characteristics=(
            "Skeptical, challenging, independent and "
            "focused on falsification."
        ),
    ),

    "Independent Reviewer": AgentRole(
        name="Independent Reviewer",
        description=(
            "Reviews the discussion independently and identifies "
            "logical gaps, missing evidence and alternative interpretations."
        ),
        characteristics=(
            "Balanced, independent, broad-minded and detail-oriented."
        ),
    ),

    "Creative Strategist": AgentRole(
        name="Creative Strategist",
        description=(
            "Generates alternative frameworks, scenarios and "
            "non-obvious solutions."
        ),
        characteristics=(
            "Creative, exploratory, unconventional and "
            "willing to challenge conventional assumptions."
        ),
    ),
}