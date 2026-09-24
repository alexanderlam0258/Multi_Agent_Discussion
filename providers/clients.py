from openai import OpenAI

from config.settings import PROVIDERS


def create_clients(
    api_keys: dict[str, str],
) -> dict[str, OpenAI]:

    clients: dict[str, OpenAI] = {}

    print("\n========== CLIENT INITIALIZATION ==========")
    print("API keys received:", list(api_keys.keys()))
    print("Configured providers:", list(PROVIDERS.keys()))

    for provider_name, api_key in api_keys.items():

        if provider_name not in PROVIDERS:
            print(
                f"WARNING: Unknown provider '{provider_name}'. "
                f"Skipping."
            )
            continue

        provider_config = PROVIDERS[provider_name]

        try:

            kwargs = {
                "api_key": api_key,
            }

            if provider_config.base_url:
                kwargs["base_url"] = provider_config.base_url

            client = OpenAI(**kwargs)

            clients[provider_name] = client

            print(
                f"SUCCESS: {provider_config.name} "
                f"client initialized."
            )

        except Exception as exc:

            print(
                f"ERROR: {provider_config.name} "
                f"client initialization failed: "
                f"{type(exc).__name__}: {exc}"
            )

    print(
        "Final client list:",
        list(clients.keys()),
    )

    print("===========================================\n")

    return clients