from enum import Enum

SPECIAL_CHARACTERS = [".", "。", ",", "，", "!",  "！", "?", "？", "%",  "－",
                      "…", "⋯",  ".", "·",  "\"", "“",  "”", "$",  "｜",]


class EntryColourPhoneticType(Enum):
    NONE = 0
    CANTONESE = 1
    MANDARIN = 2


def applyColours(original: str, tones: list[int], cantoneseToneColours: list[str], MandarinToneColours: list[str], phoneticType: EntryColourPhoneticType) -> str:
    """Adds HTML tags to each Chinese character with colours
    corresponding to the character's tone.

    Args:
        original (str): String of Chinese characters to be coloured in
        tones (list[int]): List of tone numbers
        cantoneseToneColours (list[str]): Tone colours for Cantonese
        mandarinToneColours (list[str]): Tone colours for Mandarin
        phoneticType (EntryColourPhoneticType): Language with which to colour in characters

    Returns:
        str: string of Chinese characters with HTML tags for colours
    """
    pass


def compareStrings(original: str, comparison: str) -> str:
    """Compares original and comparison, replacing Chinese
    characters that are the same between the two strings with
    a dash character

    Args:
        original (str): String of Chinese characters
        comparison (str): String of Chinese characters

    Returns:
        str: Same as "comparison" arg but characters that are the
        same between original and comparison are replaced with a dash
    """
    pass


def jyutpingToYale(jyutping: str, useSpacesToSegment: bool = False) -> str:
    """Converts Jyutping romanization to Yale romanization

    Args:
        jyutping (str): String of valid Jyutping syllables
        useSpacesToSegment (bool, optional): By default, this function
        attempts to separate Jyutping syllables via valid Jyutping finals.
        When this argument is True, disables Jyutping final detection and
        instead assumes each space-separated string is a valid Jyutping
        syllable. Defaults to False.

    Returns:
        str: String of Yale syllables
    """
    pass


def jyutpingToIPA(jyutping: str, useSpacesToSegment: bool = False) -> str:
    """Converts Jyutping romanization to Cantonese Sinological IPA

    Args:
        jyutping (str): String of valid Jyutping syllables
        useSpacesToSegment (bool, optional): By default, this function
        attempts to separate Jyutping syllables via valid Jyutping finals.
        When this argument is True, disables Jyutping final detection and
        instead assumes each space-separated string is a valid Jyutping
        syllable. Defaults to False.

    Returns:
        str: String of Cantonese Sinological IPA syllables
    """
    pass


def prettyPinyin(pinyin: str) -> str:
    """Converts raw Pinyin in database (with u: and digits for tones)
    to the conventional Hanyu Pinyin representation

    Args:
        pinyin (str): String of valid raw Pinyin syllables

    Returns:
        str: String of pretty Pinyin syllables
    """
    pass


def numberedPinyin(pinyin: str) -> str:
    """Converts raw Pinyin in database (with u:) to representation
    using the ü but retaining digits for tones

    Args:
        pinyin (str): String of valid raw Pinyin syllables

    Returns:
        str: String of numbered Pinyin syllables with ü
    """
    pass


def pinyinWithV(pinyin: str) -> str:
    """Converts raw Pinyin in database (with u:) to representation
    using "v" to represent "ü" but retaining digits for tones.

    Args:
        pinyin (str): String of valid raw Pinyin syllables

    Returns:
        str: String of numbered Pinyin syllables with v
    """
    pass


def pinyinToZhuyin(pinyin: str, useSpacesToSegment: bool = False) -> str:
    """Converts raw Pinyin in database to Zhuyin/Bopomofo.

    Args:
        pinyin (str): String of valid raw Pinyin syllables
        useSpacesToSegment (bool, optional): By default, this function
        attempts to separate Pinyin syllables via valid Pinyin finals.
        When this argument is True, disables Pinyin final detection and
        instead assumes each space-separated string is a valid Pinyin
        syllable. Defaults to False.

    Returns:
        str: String of Zhuyin syllables
    """
    pass


def pinyinToIPA(pinyin: str, useSpacesToSegment: bool = False) -> str:
    """Convert raw Pinyin in database to Mandarin Sinological IPA.

    Args:
        pinyin (str): String of valid raw Pinyin syllables
        useSpacesToSegment (bool, optional): By default, this function
        attempts to separate Pinyin syllables via valid Pinyin finals.
        When this argument is True, disables Pinyin final detection and
        instead assumes each space-separated string is a valid Pinyin
        syllable. Defaults to False.

    Returns:
        str: String of Mandarin Sinological IPA syllables
    """
    pass
