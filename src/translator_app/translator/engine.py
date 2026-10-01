import requests

from .languages import AUTO_DETECT

DEFAULT_SOURCE = AUTO_DETECT
DEFAULT_TARGET = "pt"

# Same free endpoint served from two hosts: if Google blocks one (429 / "sorry"
# page), the other usually still answers.
TRANSLATE_URLS = (
    "https://translate.googleapis.com/translate_a/single",
    "https://translate.google.com/translate_a/single",
)


class TranslationError(Exception):
    pass


def translate(text: str, source: str = DEFAULT_SOURCE, target: str = DEFAULT_TARGET) -> str:
    text = text.strip()
    if not text:
        return ""

    params = {
        "client": "gtx",
        "sl": source,
        "tl": target,
        "dt": "t",
        "q": text,
    }

    last_error = None
    for url in TRANSLATE_URLS:
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            return "".join(chunk[0] for chunk in data[0] if chunk[0])
        except requests.RequestException as e:
            last_error = TranslationError(str(e))
        except (ValueError, KeyError, IndexError, TypeError) as e:
            last_error = TranslationError(f"Unexpected response format: {e}")

    raise last_error
