from deep_translator import GoogleTranslator

def translate_en(text):
    try:
        return GoogleTranslator(source="auto", target="en").translate(text)
    except Exception:
        return text

def translate_ru(text):
    try:
        return GoogleTranslator(source="auto", target="ru").translate(text)
    except Exception:
        return text
