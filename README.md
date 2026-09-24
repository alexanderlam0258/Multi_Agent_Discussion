# 🏛️ Multi-Agent Discussion Council

### A configurable AI council where different models debate, challenge, and synthesize complex questions.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-red.svg)](https://streamlit.io/)
[![OpenAI Compatible](https://img.shields.io/badge/API-OpenAI%20Compatible-green.svg)](https://platform.openai.com/)

---

## 💡 What is this?

**Multi-Agent Discussion Council** is an experimental AI reasoning platform that brings multiple AI models together as a structured discussion council.

Instead of asking a single AI for an answer, the system assigns different models different analytical roles:

| Role | Purpose |
|---|---|
| 🔎 Evidence Analyst | Examines facts, evidence and assumptions |
| 📊 Analytical Lead | Builds the main analytical framework |
| ⚔️ Adversarial Critic | Challenges assumptions and conclusions |
| 🧭 Independent Reviewer | Looks for gaps and alternative interpretations |
| 💡 Creative Strategist | Generates unconventional perspectives |
| 👑 Chairman | Synthesizes the entire discussion |

The models do **not** need to come from the same provider.

For example:

```text
             ┌──────────────────┐
             │   Discussion     │
             │      Topic       │
             └────────┬─────────┘
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
   🔎 Evidence    ⚔️ Critic    💡 Strategist
      Analyst
        │             │             │
        └─────────────┼─────────────┘
                      ▼
              🧭 Independent
                 Reviewer
                      │
                      ▼
               👑 Chairman
                      │
                      ▼
              Final Synthesis