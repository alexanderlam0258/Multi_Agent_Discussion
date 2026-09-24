

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

```
---
## 📝 Discussion Brief

Before starting a discussion, the user provides three key pieces of information.

Discussion Topic

The main question or issue to be discussed.

Background Context

Relevant information, assumptions, constraints, or circumstances that the agents should understand.

Discussion Rules

Rules that guide how the agents should participate.

For example:

Challenge assumptions.
Distinguish facts from opinions.
Consider opposing evidence.
Avoid simply repeating previous arguments.
Identify uncertainty.
Explain important assumptions.
Introduce alternative interpretations where appropriate.

These instructions are incorporated into the agents' discussion context.

---
## 🤖 Discussion Agents

Each discussion agent can be configured independently.

The user can select:

Role
Provider
Model
Characteristics

For example:

### 🔎 Evidence Analyst

Focuses on:

Facts
Evidence
Data
Sources
Assumptions
Reliability
### 📊 Analytical Lead

Focuses on:

Analytical frameworks
Structured reasoning
Connecting evidence
Synthesis
### ⚔️ Adversarial Critic

Focuses on:

Challenging assumptions
Identifying weaknesses
Constructing counterarguments
Testing conclusions

### 🧭 Independent Reviewer

Focuses on:

Logical gaps
Missing evidence
Alternative interpretations
Independent assessment
### 💡 Creative Strategist

Focuses on:

Alternative frameworks
Scenarios
Unconventional approaches
Non-obvious solutions

These roles are starting defaults and can be expanded as the project develops.

### 👑 Chairman

The Chairman is a separate AI participant responsible for synthesizing the discussion.

The Chairman can independently use a different:

Provider
Model
Set of characteristics

The Chairman is not hard-coded to a particular AI provider.

The Chairman should not simply count votes or select the opinion expressed by the majority.

Instead, it should:
1. Identify major areas of agreement.
2. Identify substantive disagreements.
3. Distinguish factual claims from interpretations.
4. Identify important assumptions.
5. Identify weaknesses in the arguments.
6. Identify unresolved questions.
7. Present the strongest arguments from different perspectives.
8. Produce a coherent final synthesis.

---
## 🔄 Chairman Fallback

The Chairman can be configured with a fallback provider/model.


For example:
```text
Primary Chairman
OpenRouter / Model A
        │
        │ failure
        ▼
Fallback Chairman
Gemini / Model B
```
This is useful when experimenting with models that may have:

1. Temporary availability problems
2. Rate limits
3. Quota limitations
4. Credit limitations
5. Model availability issues
6. Other API failures

The fallback mechanism is intended to make the discussion more resilient.

---
## 🛡️ Provider Failure Handling

A key design principle is that one provider failure should not normally terminate the entire discussion.

For example:

Gemini        → Available
OpenRouter    → Available
DeepSeek      → Available
Grok          → Unavailable
OpenAI        → Unavailable

The application should continue using the providers that remain available.

Similarly, if an individual discussion agent fails during a round, the application should record the failure and allow the remaining agents to continue where possible.

---
## 🔍 Dynamic Model Discovery

The application discovers available models when it starts.

The general process is:
```text
API Key
   ↓
Create Provider Client
   ↓
Query Available Models
   ↓
Filter Non-Discussion Models
   ↓
Available Models
   ↓
User Selection
```

Models intended for functions such as embeddings, image generation, audio, moderation, or reranking can be excluded from discussion-model selection.

This approach reduces the need to manually maintain model lists.

---
## 🚀 Quick Start
1. Clone the Repository
git clone <YOUR_REPOSITORY_URL>
cd Mulit_agent_discussion

Replace <YOUR_REPOSITORY_URL> with the URL of your GitHub repository.

2. Create a Python Environment

A Conda environment is recommended.

For example:

conda create -n multi-agent-discussion python=3.11
conda activate multi-agent-discussion

The Python environment should remain outside the Git repository.

3. Install Dependencies

Run:

pip install -r requirements.txt

4. Configure API Keys

API keys should be stored outside the Git repository.

The current development configuration uses:

\\API_Keys\\api_keys.csv

The expected format is:

Provider,API_Key
Gemini,<YOUR_GEMINI_API_KEY>
GPT,<YOUR_OPENAI_API_KEY>
Grok,<YOUR_GROK_API_KEY>
Deepseek,<YOUR_DEEPSEEK_API_KEY>
OpenRouter,<YOUR_OPENROUTER_API_KEY>

You do not need to configure every provider.

If a provider does not have an API key, it can simply be skipped.

A provider with a valid API key may still be unavailable because of account permissions, credits, quotas, model availability, or other provider-side restrictions.

5. Start the Application

Run:

python -m streamlit run app.py

The Streamlit application should then open in your browser.

For the current Windows development environment:

cd /d F:\Mulit_agent_discussion
conda activate F:\conda_envs\Mulit_agent_discussion
python -m streamlit run app.py

---
## 📁 Project Structure
```text
Mulit_agent_discussion/
│
├── app.py
│
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── api_keys.py
│   └── agents.py
│
├── providers/
│   ├── __init__.py
│   ├── clients.py
│   └── models.py
│
├── council/
│   ├── __init__.py
│   └── discussion.py
│
├── ui/
│   ├── __init__.py
│   ├── sidebar.py
│   └── setup.py
│
├── requirements.txt
├── README.md
├── description.md
└── .gitignore
```
Main Components

#### app.py

Main Streamlit application and discussion orchestration.

#### config/

Configuration, provider definitions, API-key loading, and agent roles.

#### providers/

Provider client initialization and dynamic model discovery.

#### council/

Discussion logic, agent turns, and Chairman synthesis.

#### ui/

Streamlit interface components.

#### description.md

Detailed project architecture, requirements, design principles, and future development plans.

---
## 🔐 Security

Never commit API keys to GitHub.

The following types of files should remain outside the repository:

api_keys.csv
.env
.streamlit/secrets.toml

API credentials should never be placed directly into source code.

Before pushing changes to GitHub, check:

git status

Make sure no API-key files or other secrets are included.

---
## 🧪 Project Status

Active Development

The project is currently under active development.

1. Current Focus
2. Dynamic model discovery
3. Configurable agent roles
4. Provider/model selection
5. Multi-round discussion
6. Chairman synthesis
7. Provider failure handling
8. Chairman fallback
9. OpenRouter integration
10. Planned / Future Development
11. Agent-level fallback
12. Parallel agent execution
13. Cost tracking
14. Persistent discussions
15. Discussion export
16. Custom user-defined roles
17. Model capability comparison
18. Model cost comparison
19. Improved discussion history and replay
20. More sophisticated Chairman analysis

---
## 📖 Documentation

For a more detailed description of the system architecture and design requirements:

Read the Project Description

For Python dependencies:

View Requirements

---
## 🧠 Design Philosophy

The project is intended to be more than a simple multi-chat interface.

The central idea is:

Different Models
       +
Different Analytical Roles
       +
Structured Discussion
       +
Adversarial Challenge
       +
Independent Review
       ↓
Chairman Synthesis

Different models may have different strengths, weaknesses, assumptions, and reasoning styles.

Rather than trying to eliminate those differences, the system uses them as part of the discussion process.

The objective is to make disagreement useful.

A good discussion should expose:

Competing arguments
Hidden assumptions
Weak reasoning
Missing evidence
Alternative interpretations
Unresolved uncertainty

before the final synthesis is produced.

---
## ⚠️ Disclaimer

This is an experimental multi-agent AI discussion framework.

AI-generated content may be incorrect, incomplete, outdated, or contradictory.

The application should therefore be treated as a reasoning and discussion aid rather than an authoritative source of truth.

Important conclusions should be independently verified, particularly when they involve financial, legal, medical, technical, or other high-impact decisions.