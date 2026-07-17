from deep_translator import GoogleTranslator

SOURCE_LANG = "en"
TARGET_LANG = "pt"


class TranslationError(Exception):
    pass


def translate(text: str) -> str:
    text = text.strip()
    if not text:
        return ""

    try:
        return GoogleTranslator(source=SOURCE_LANG, target=TARGET_LANG).translate(text)
    except Exception as e:
        raise TranslationError(str(e)) from e
