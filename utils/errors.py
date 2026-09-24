def format_provider_error(
    provider: str,
    exc: Exception,
) -> str:

    return (
        f"{provider.upper()} unavailable: "
        f"{type(exc).__name__}: {exc}"
    )