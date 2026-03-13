import os
from gettext import translation

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOCALES_DIR = os.path.join(BASE_DIR, "locales")

def get_translator(lang: str):
    try:
        translator = translation(
            "messages",
            localedir=LOCALES_DIR,
            languages=[lang],
            fallback=True
        )
    except Exception:
        translator = translation(
            "messages",
            localedir=LOCALES_DIR,
            languages=["en"],
            fallback=True
        )

    return translator.gettext