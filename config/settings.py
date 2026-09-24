from dataclasses import dataclass


@dataclass(frozen=True)
class ProviderConfig:
    name: str
    base_url: str | None
    api_key_name: str


PROVIDERS = {

    "gemini": ProviderConfig(
        name="Gemini",
        base_url=(
            "https://generativelanguage.googleapis.com/"
            "v1beta/openai/"
        ),
        api_key_name="gemini",
    ),

    "gpt": ProviderConfig(
        name="OpenAI",
        base_url=None,
        api_key_name="gpt",
    ),

    "grok": ProviderConfig(
        name="Grok",
        base_url="https://api.x.ai/v1",
        api_key_name="grok",
    ),

    "deepseek": ProviderConfig(
        name="DeepSeek",
        base_url="https://api.deepseek.com",
        api_key_name="deepseek",
    ),

    "openrouter": ProviderConfig(
        name="OpenRouter",
        base_url="https://openrouter.ai/api/v1",
        api_key_name="openrouter",
    ),
}