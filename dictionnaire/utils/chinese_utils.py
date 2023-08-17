from enum import Enum
from unicodedata import normalize

SPECIAL_CHARACTERS = (".", "。", ",", "，", "!",  "！", "?", "？", "%",  "－",
                      "…", "⋯",  ".", "·",  "\"", "“",  "”", "$",  "｜",)

JYUTPING_INITIALS = ("b",  "p", "m",  "f",  "d",
                     "t",  "n", "l",  "g",  "k",
                     "ng", "h", "gw", "kw", "w",
                     "z",  "c", "s",  "j",  "m")

JYUTPING_FINALS = ("a",   "aa",  "aai", "aau", "aam", "aan", "aang", "aap", "aat",
                   "aak", "ai",  "au",  "am",  "an",  "ang", "ap",   "at",  "ak",
                   "e",   "ei",  "eu",  "em",  "en",  "eng", "ep",   "ek",  "i",
                   "iu",  "im",  "in",  "ing", "ip",  "it",  "ik",   "o",   "oi",
                   "ou",  "on",  "ong", "ot",  "ok",  "u",   "ui",   "un",  "ung",
                   "ut",  "uk",  "oe",  "oet", "eoi", "eon", "oeng", "eot", "oek",
                   "yu",  "yun", "yut", "m",   "ng")

JYUTPING_TONES = (1, 2, 3, 4, 5, 6)

PINYIN_INITIALS = ("b", "p", "m",  "f",  "d",  "t",
                   "n", "l", "g",  "k",  "h",  "j",
                   "q", "x", "zh", "ch", "sh", "r",
                   "z", "c", "s")

PINYIN_FINALS = ("a",   "e",   "ai",   "ei",   "ao",   "ou", "an", "ang", "en",
                 "ang", "eng", "ong",  "er",   "i",    "ia", "ie", "iao", "iu",
                 "ian", "in",  "iang", "ing",  "iong", "u",  "ua", "uo",  "uai",
                 "ui",  "uan", "un",   "uang", "u",    "u:", "ue", "u:e", "o")

PINYIN_TONES = (1, 2, 3, 4, 5)

SAME_CHARACTER_STRING = "－"


def extract_jyutping_tones(string: str) -> list[int]:
    """Get the list of tones from a valid Jyutping string

    Args:
        string (str): String of valid Jyutping syllables

    Returns:
        list[int]: A list of the tones in those syllables
    """
    res = []
    for c in string:
        if c.isnumeric() and int(c) in JYUTPING_TONES:
            res.append(int(c))
    return res


def extract_pinyin_tones(string: str) -> list[int]:
    """Get the list of tones from a valid Pinyin string

    Args:
        string (str): String of valid Pinyin syllables

    Returns:
        list[int]: A list of the tones in those syllables
    """
    res = []
    for c in string:
        if c.isnumeric() and int(c) in PINYIN_TONES:
            res.append(int(c))
    return res


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
        res += f"<span style=\"color: {tone_colours[tone]}\">{codepoint}</span>"
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

    original, comparison = normalize(
        "NFC", original), normalize("NFC", comparison)
    for idx, codepoint in enumerate(original):
        res += codepoint if original[idx] == comparison[idx] else SAME_CHARACTER_STRING
    return res


def jyutping_to_yale(jyutping: str, useSpacesToSegment: bool = False) -> str:
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


def jyutping_to_IPA(jyutping: str, useSpacesToSegment: bool = False) -> str:
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


def pretty_pinyin(pinyin: str) -> str:
    """Converts raw Pinyin in database (with u: and digits for tones)
    to the conventional Hanyu Pinyin representation

    Args:
        pinyin (str): String of valid raw Pinyin syllables

    Returns:
        str: String of pretty Pinyin syllables
    """
    pass


def numbered_pinyin(pinyin: str) -> str:
    """Converts raw Pinyin in database (with u:) to representation
    using the ü but retaining digits for tones

    Args:
        pinyin (str): String of valid raw Pinyin syllables

    Returns:
        str: String of numbered Pinyin syllables with ü
    """
    pass


def pinyin_with_v(pinyin: str) -> str:
    """Converts raw Pinyin in database (with u:) to representation
    using "v" to represent "ü" but retaining digits for tones.

    Args:
        pinyin (str): String of valid raw Pinyin syllables

    Returns:
        str: String of numbered Pinyin syllables with v
    """
    pass


def pinyin_to_zhuyin(pinyin: str, useSpacesToSegment: bool = False) -> str:
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


def pinyin_to_IPA(pinyin: str, useSpacesToSegment: bool = False) -> str:
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


def segment_jyutping(string: str, remove_special_characters: bool = True,
                     remove_glob_characters: bool = True) -> list[str]:
    """Segments Jyutping by looking at valid Jyutping initials and finals.
    Can be configured to remove special characters and/or
    wildcard delimiter (glob) characters.

    Args:
        string (str): String of valid Jyutping syllables, possibly with
            special characters or glob characters
        removeSpecialCharacters (bool, optional): Do not include special
            characters in output list. Defaults to True.
        removeGlobCharacters (bool, optional): Do not include glob characters
            in output list. Defaults to True.

    Returns:
        list[str]: List where each string is a valid Jyutping syllable,
            special character, or glob character
    """
    string = string.lower()
    start_idx, end_idx, initial_found = 0, 0, False
    res = []

    while end_idx < len(string):
        component_found = False

        curr_string = string[end_idx]
        is_special_character = curr_string in SPECIAL_CHARACTERS
        is_glob_character = (curr_string.strip() == "*"
                             or curr_string.strip() == "?")

        if (curr_string == " " or curr_string == "'"
                or is_special_character or is_glob_character):
            if initial_found:
                # Whitespace, apostrophes, special characters, and glob
                # characters mean that we *must* split a syllable
                syllable = string[start_idx:end_idx]
                res.append(syllable)
                start_idx = end_idx
                initial_found = False

            if not remove_glob_characters and is_glob_character:
                # Whitespace matters for glob characters! Consume
                # the next or previous whitespace if it exists and the
                # whitespace was not consumed by another syllable
                glob_start_idx = end_idx
                glob_end_idx = glob_start_idx + 1

                if ((end_idx >= 1) and (string[end_idx - 1] == " ")
                        and (res and res[-1][-1] != " ")):
                    # Keep whitespace preceding the glob character ONLY IF
                    # whitespace was not already added to the previous syllable
                    glob_start_idx -= 1
                if ((len(string) > (end_idx + 1))
                        and (string[end_idx + 1] == " ")):
                    # If there is whitespace succeeding the glob character,
                    # add it to this syllable, and mark the whitespace as
                    # being consumed by incrementing end_idx
                    glob_end_idx += 1
                    end_idx += 1

                glob_str = string[glob_start_idx:glob_end_idx]
                res.append(glob_str)

                start_idx = end_idx
            elif not remove_special_characters and is_special_character:
                special_char = curr_string
                res.append(special_char)

            start_idx += 1
            end_idx += 1
            continue

        if curr_string.isnumeric():
            # Digits are only valid after a final, or after an initial
            # that functions as a final (such as m or ng). This block
            # checks for the latter case.
            if initial_found:
                initial = string[start_idx:end_idx]
                if initial in JYUTPING_FINALS:
                    initial_with_digit = initial + curr_string
                    res.append(initial_with_digit)
                    end_idx += 1
                    start_idx = end_idx
                    initial_found = False
                    continue

        for initial_len in range(2, 0, -1):
            # Initials can be length 2 or less; check for longer initials
            # before checking for shorter initials
            curr_string = string[end_idx:end_idx+initial_len]

            if curr_string not in JYUTPING_INITIALS:
                continue

            if initial_found:
                # Multiple initials in a row are only valid if what the
                # algorithm initially analyzed as an initial was actually
                # a final.
                # This might happen for a string like (mgoi), where "m" could
                # be parsed as an initial followed by "g" as an initial.
                # In this case, the first initial is a valid syllable if it
                # can be a syllable per se; in that case, it would also be
                # a member of JYUTPING_FINALS
                first_initial = string[start_idx:end_idx]
                if first_initial in JYUTPING_FINALS:
                    res.append(first_initial)
                    start_idx = end_idx

            end_idx += initial_len
            initial_found = True
            component_found = True

        if component_found:
            continue

        for final_len in range(4, 0, -1):
            # Finals (nucleus + coda) can be length 4 or less; check for longer
            # finals before checking for shorter finals
            curr_string = string[end_idx:end_idx+final_len]
            if curr_string in JYUTPING_FINALS:
                end_idx += final_len
                if end_idx < len(string):
                    if string[end_idx].isnumeric():
                        # Append the tone digit following the final to the
                        # syllable
                        end_idx += 1
                syllable = string[start_idx:end_idx]
                res.append(syllable)
                start_idx = end_idx
                component_found = True
                initial_found = False
                break

        if component_found:
            continue

        end_idx += 1

    # Add whatever's left in the search term, minus whitespace
    last_word = string[start_idx:]
    last_word = ' '.join(last_word.split())
    last_word = last_word.strip()
    if last_word and last_word != "'":
        res.append(last_word)

    return res


def segment_pinyin(string: str, remove_special_characters: bool = True,
                   remove_glob_characters: bool = True) -> list[str]:
    """Segments Pinyin by looking at valid Pinyin initials and finals.
    Can be configured to remove special characters and/or
    wildcard delimiter (glob) characters.

    Args:
        string (str): String of valid Pinyin syllables, possibly with special
            characters or glob characters
        removeSpecialCharacters (bool, optional): Do not include special
            characters in output list. Defaults to True.
        removeGlobCharacters (bool, optional): Do not include glob characters
            in output list. Defaults to True.

    Returns:
        list[str]: List where each string is a valid Pinyin syllable, special
            character, or glob character
    """
    string = string.lower()
    start_idx, end_idx, initial_found = 0, 0, False
    res = []

    while end_idx < len(string):
        component_found = False

        curr_string = string[end_idx]
        is_special_character = curr_string in SPECIAL_CHARACTERS
        is_glob_character = (curr_string.strip() == "*"
                             or curr_string.strip() == "?")

        if (curr_string == " " or curr_string == "'"
                or is_special_character or is_glob_character):
            if initial_found:
                # Whitespace, apostrophes, special characters, and glob
                # characters mean that we *must* split a syllable
                syllable = string[start_idx:end_idx]
                res.append(syllable)
                start_idx = end_idx
                initial_found = False

            if not remove_glob_characters and is_glob_character:
                # Whitespace matters for glob characters! Consume
                # the next or previous whitespace if it exists and the
                # whitespace was not consumed by another syllable
                glob_start_idx = end_idx
                glob_end_idx = glob_start_idx + 1

                if ((end_idx >= 1) and (string[end_idx - 1] == " ")
                        and (res and res[-1][-1] != " ")):
                    # Keep whitespace preceding the glob character ONLY IF
                    # whitespace was not already added to the previous syllable
                    glob_start_idx -= 1
                if ((len(string) > (end_idx + 1))
                        and (string[end_idx + 1] == " ")):
                    # If there is whitespace succeeding the glob character,
                    # add it to this syllable, and mark the whitespace as
                    # being consumed by incrementing end_idx
                    glob_end_idx += 1
                    end_idx += 1

                glob_str = string[glob_start_idx:glob_end_idx]
                res.append(glob_str)

                start_idx = end_idx
            elif not remove_special_characters and is_special_character:
                special_char = curr_string
                res.append(special_char)

            start_idx += 1
            end_idx += 1
            continue

        for initial_len in range(2, 0, -1):
            # Initials can be length 2 or less; check for longer initials
            # before checking for shorter initials
            curr_string = string[end_idx:end_idx+initial_len]
            if curr_string in PINYIN_INITIALS:
                end_idx += initial_len
                component_found = True
                initial_found = True
                break

        if component_found:
            continue

        for final_len in range(4, 0, -1):
            # Finals (nucleus + coda) can be length 4 or less; check for longer
            # finals before checking for shorter finals
            curr_string = string[end_idx:end_idx+final_len]
            if curr_string in PINYIN_FINALS:
                end_idx += final_len
                if end_idx < len(string):
                    if string[end_idx].isnumeric():
                        # Append the tone digit following the final to the
                        # syllable
                        end_idx += 1
                syllable = string[start_idx:end_idx]
                res.append(syllable)
                start_idx = end_idx
                component_found = True
                initial_found = False
                break

        if component_found:
            continue

        end_idx += 1

    # Add whatever's left in the search term, minus whitespace
    last_word = string[start_idx:]
    last_word = ' '.join(last_word.split())
    last_word = last_word.strip()
    if last_word and last_word != "'":
        res.append(last_word)

    return res
