from deep_translator import GoogleTranslator

from .languages import AUTO_DETECT

DEFAULT_SOURCE = AUTO_DETECT
DEFAULT_TARGET = "pt"


class TranslationError(Exception):
    pass


def translate(text: str, source: str = DEFAULT_SOURCE, target: str = DEFAULT_TARGET) -> str:
    text = text.strip()
    if not text:
        return ""

    try:
        return GoogleTranslator(source=source, target=target).translate(text)
    except Exception as e:
        raise TranslationError(str(e)) from e
