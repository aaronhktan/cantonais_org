def constructRomanisationQuery(words: list[str], delimiter: str) -> str:
    """Appends wildcard delimiter to each syllable if the syllable does
    not end with a digit.

    Args:
        words (list[str]): List of syllables
        delimiter (str): Character to append to each syllable

    Returns:
        str: All syllables in word list with appended wildcard delimiter
    """
    pass


def segmentPinyin(string: str, removeSpecialCharacters: bool = True, removeGlobCharacters: bool = True) -> list[str]:
    """Segments Pinyin by looking at valid Pinyin initials and finals.
    Can be configured to remove special characters and/or
    wildcard delimiter (glob) characters.

    Args:
        string (str): String of valid Pinyin syllables, possibly with special characters or glob characters
        removeSpecialCharacters (bool, optional): Do not include special characters in output list. Defaults to True.
        removeGlobCharacters (bool, optional): Do not include glob characters in output list. Defaults to True.

    Returns:
        list[str]: List where each string is a valid Pinyin syllable, special character, or glob character
    """
    pass


def segmentJyutping(string: str, removeSpecialCharacters: bool = True, removeGlobCharacters: bool = True) -> list[str]:
    """Segments Jyutping by looking at valid Jyutping initials and finals.
    Can be configured to remove special characters and/or
    wildcard delimiter (glob) characters.

    Args:
        string (str): String of valid Jyutping syllables, possibly with special characters or glob characters
        removeSpecialCharacters (bool, optional): Do not include special characters in output list. Defaults to True.
        removeGlobCharacters (bool, optional): Do not include glob characters in output list. Defaults to True.

    Returns:
        list[str]: List where each string is a valid Jyutping syllable, special character, or glob character
    """
    pass
