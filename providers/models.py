from openai import OpenAI


EXCLUDED_MODEL_TERMS = {
    "embedding",
    "embed",
    "moderation",
    "whisper",
    "tts",
    "image",
    "audio",
    "rerank",
}


def discover_models(
    client: OpenAI,
    provider_name: str,
) -> tuple[list[str], str | None]:

    try:

        response = client.models.list()

        models = []

        for model in response.data:

            model_id = getattr(
                model,
                "id",
                None,
            )

            if not model_id:
                continue

            model_lower = model_id.lower()

            if any(
                term in model_lower
                for term in EXCLUDED_MODEL_TERMS
            ):
                continue

            models.append(model_id)

        # OpenRouter special handling.
        #
        # This allows the user to use the free router even
        # if the exact free-model list changes.
        if provider_name == "openrouter":

            if "openrouter/free" not in models:
                models.insert(
                    0,
                    "openrouter/free",
                )

        if not models:

            return (
                [],
                "No usable text-generation models were found."
            )

        return sorted(
            set(models),
            key=lambda x: (
                0 if x == "openrouter/free" else 1,
                0 if ":free" in x else 1,
                x.lower(),
            ),
        ), None

    except Exception as exc:

        return (
            [],
            f"{type(exc).__name__}: {exc}",
        )


def discover_all_models(
    clients: dict[str, OpenAI],
) -> tuple[
    dict[str, list[str]],
    dict[str, str],
]:

    available_models: dict[str, list[str]] = {}
    provider_errors: dict[str, str] = {}

    for provider_name, client in clients.items():

        models, error = discover_models(
            client,
            provider_name,
        )

        if models:

            available_models[provider_name] = models

        else:

            provider_errors[provider_name] = (
                error or "Unknown provider error."
            )

    return (
        available_models,
        provider_errors,
    )