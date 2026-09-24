# Multi-Agent Discussion Council

## 1. Project Overview

Multi-Agent Discussion Council is a configurable AI discussion platform built with Streamlit.

The system allows multiple AI agents, potentially powered by different AI providers and models, to participate in a structured discussion on a user-defined topic.

A separate AI Chairman then reviews the discussion and produces a final synthesis.

The core design principle is:

> **Provider, model, and discussion role are independent concepts.**

This allows the user to freely combine different AI models and assign them different analytical roles.

For example:

- Gemini → Evidence Analyst
- OpenRouter → Creative Strategist
- DeepSeek → Adversarial Critic
- OpenAI → Independent Reviewer
- another available model → Chairman

The actual configuration should depend on which providers and models are currently available.

---

# 2. Main Objectives

The application is intended to provide a flexible environment for structured multi-model reasoning.

The major objectives are:

1. Support multiple AI providers.
2. Discover available models dynamically.
3. Allow providers to be enabled or disabled independently.
4. Allow discussion roles to be assigned independently of providers.
5. Allow users to configure agent characteristics.
6. Allow users to select the Chairman provider and model.
7. Support fallback models/providers when a selected model fails.
8. Continue the discussion when an individual agent fails.
9. Provide clear diagnostics when a provider is unavailable.
10. Keep API credentials outside the GitHub repository.
11. Provide a simple Streamlit interface for configuring and running discussions.

---

# 3. Supported Providers

The initial architecture supports the following providers:

- OpenAI
- Google Gemini
- xAI Grok
- DeepSeek
- OpenRouter

Providers use an internal lowercase identifier:

```text
openai  → gpt
gemini
grok
deepseek
openrouter