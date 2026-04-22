from src.messages import get_messages, normalize_language


def test_normalize_language_aliases():
    assert normalize_language('EN') == 'en'
    assert normalize_language('spanish') == 'spanish'
    assert normalize_language('unknown') == 'en'


def test_get_messages_falls_back_to_english():
    messages = get_messages('unknown')
    assert messages['help'].startswith('Commands:')


def test_get_messages_returns_spanish_catalog():
    messages = get_messages('es')
    assert messages['help'].startswith('Comandos:')