
import fugashi

tagger = fugashi.Tagger()

def katakana_to_hiragana(text: str) -> str:
    """
    Convert Katakana to Hiragana using Fugashi.
    """

    return "".join(chr(ord(char) - 0x60) if 'ァ' <= char <= 'ヶ' else char for char in text)


def contains_kanji(text: str) -> bool:
    return any ("一" <= char <= "龯" for char in text)


def analyze_text(text: str) -> list[dict]:
    tokens = []

    for word in tagger(text):
        surface = word.surface
        has_kanji = contains_kanji(surface)

        if has_kanji:
            reading_katakana = word.feature.kana or word.feature.pron or surface 
            reading = katakana_to_hiragana(reading_katakana)
        else:
            reading = surface

        tokens.append({
            "surface": surface,
            "reading": reading,
            "has_kanji": has_kanji
        })

    return tokens