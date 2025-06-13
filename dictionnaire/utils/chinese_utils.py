from unicodedata import normalize

SPECIAL_CHARACTERS = (
    ".",
    "。",
    ",",
    "，",
    "!",
    "！",
    "?",
    "？",
    "%",
    "－",
    "…",
    "⋯",
    ".",
    "·",
    '"',
    "“",
    "”",
    "$",
    "｜",
)

SAME_CHARACTER_STRING = "－"


def apply_colours(original: str, tones: list[int], tone_colours: list[str]) -> str:
    """Adds HTML tags to each Chinese character with colours
    corresponding to the character's tone.

    Args:
        original (str): String of Chinese characters to be coloured in
        tones (list[int]): List of tone numbers
        ton_colours (list[str]): RGB tone colours
        phoneticType (EntryColourPhoneticType): Language with which to colour
            in characters

    Returns:
        str: string of Chinese characters with HTML tags for colours
    """
    res = ""
    tone_idx = 0

    for codepoint in original:
        if codepoint == SAME_CHARACTER_STRING:
            # Don't add colours to the same character string
            # But since they represent a character, increment the tone index
            res += codepoint
            tone_idx += 1
            continue

        is_alphabetic = codepoint.isupper() or codepoint.islower()
        if codepoint in SPECIAL_CHARACTERS or is_alphabetic:
            # Don't add colours to special characters or letters
            # because the dictionary doesn't have tones for them
            res += codepoint
            continue

        if tone_idx >= len(tones):
            res += codepoint
            continue

        tone = tones[tone_idx]
        res += f'<span style="color: {tone_colours[tone]}">{codepoint}</span>'
        tone_idx += 1

    return res


def compare_strings(original: str, comparison: str) -> str:
    """Compares original and comparison, replacing Chinese
    characters that are the same between the two strings with
    a dash character

    This function **DOES NOT** compare graphemes - it only
    compares code points! It also normalizes Unicode codepoints
    using NFC normalization.

    Args:
        original (str): String of Chinese characters
        comparison (str): String of Chinese characters

    Returns:
        str: Same as "comparison" arg but characters that are the
        same between original and comparison are replaced with a dash
    """
    res = ""

    original, comparison = normalize("NFC", original), normalize("NFC", comparison)
    for idx, codepoint in enumerate(original):
        if idx < len(original) and idx < len(comparison):
            res += (
                SAME_CHARACTER_STRING
                if (original[idx] == comparison[idx])
                else comparison[idx]
            )
        else:
            res += original[idx]
    return res
