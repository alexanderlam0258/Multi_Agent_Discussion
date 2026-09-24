import csv
from pathlib import Path

from config.settings import PROVIDERS


API_KEY_FILE = Path(r"F:\API_Keys\api_keys.csv")


def load_api_keys(
    file_path: Path = API_KEY_FILE,
) -> dict[str, str]:

    if not file_path.exists():
        raise FileNotFoundError(
            f"API key file does not exist: {file_path}"
        )

    if not file_path.is_file():
        raise FileNotFoundError(
            f"API key path is not a file: {file_path}"
        )

    api_keys: dict[str, str] = {}

    with file_path.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as file:

        reader = csv.reader(file)

        for line_number, row in enumerate(reader, start=1):

            if not row:
                continue

            if len(row) < 2:
                raise ValueError(
                    f"Invalid API key file format at "
                    f"line {line_number}. "
                    f"Expected: Provider,API_Key"
                )

            provider = row[0].strip().lower()
            api_key = row[1].strip()

            if not provider:
                continue

            if not api_key:
                continue

            if provider not in PROVIDERS:
                # Unknown providers are ignored.
                # This allows you to keep extra keys in the CSV.
                continue

            api_keys[provider] = api_key

    return api_keys