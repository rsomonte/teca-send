from src.messages.en import MESSAGES as EN_MESSAGES
from src.messages.es import MESSAGES as ES_MESSAGES

DEFAULT_LANGUAGE = 'en'
LANGUAGE_ALIASES = {
    'en': EN_MESSAGES,
    'english': EN_MESSAGES,
    'master': EN_MESSAGES,
    'es': ES_MESSAGES,
    'spanish': ES_MESSAGES,
}


def normalize_language(language: str | None) -> str:
    if not language:
        return DEFAULT_LANGUAGE

    normalized = language.strip().lower()
    if normalized in LANGUAGE_ALIASES:
        return normalized

    return DEFAULT_LANGUAGE


def get_messages(language: str | None):
    normalized = normalize_language(language)
    return LANGUAGE_ALIASES[normalized]