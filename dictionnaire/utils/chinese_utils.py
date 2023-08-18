import re
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

YALE_INITIAL_REGEX = ((re.compile(r"^jy?"), "y"),
                      (re.compile(r"^z"), "j"),
                      (re.compile(r"^c"), "ch"),)

YALE_FINAL_REGEX = re.compile(r"([aeiou][aeiou]?[iumngptk]?[g]?)([1-6])")
YALE_LIGHT_TONE_REGEX = re.compile(r"([ptkmn]?g?)[123456]$")

YALE_SPECIAL_FINALS = {
    "aa": "a",
    "oe": "eu",
    "oeng": "eung",
    "oek": "euk",
    "eoi": "eui",
    "eon": "eun",
    "eot": "eut",
}

YALE_SPECIAL_SYLLABLES = {
    "m": ("m̄", "ḿ", "m", "m̀h", "ḿh", "mh"),
    "ng": ("n̄g", "ńg", "ng", "ǹgh", "ńgh", "ngh"),
}

YALE_VOWEL_REPLACEMENTS = {
    "a": ("ā", "á", "a", "à", "á", "a"),
    "e": ("ē", "é", "e", "è", "é", "e"),
    "i": ("ī", "í", "i", "ì", "í", "i"),
    "o": ("ō", "ó", "o", "ò", "ó", "o"),
    "u": ("ū", "ú", "u", "ù", "ú", "u"),
}

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


def extract_jyutping_tones(jyutping: str) -> list[int]:
    """Get the list of tones from a valid Jyutping string

    Args:
        jyutping (str): String of valid Jyutping syllables

    Returns:
        list[int]: A list of the tones in those syllables
    """
    res = []
    for c in jyutping:
        if c.isnumeric() and int(c) in JYUTPING_TONES:
            res.append(int(c))
    return res


def extract_pinyin_tones(pinyin: str) -> list[int]:
    """Get the list of tones from a valid Pinyin string

    Args:
        pinyin (str): String of valid Pinyin syllables

    Returns:
        list[int]: A list of the tones in those syllables
    """
    res = []
    for c in pinyin:
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
        res += (SAME_CHARACTER_STRING if original[idx]
                == comparison[idx] else comparison[idx])
    return res


def jyutping_to_yale(jyutping: str,
                     use_spaces_to_segment: bool = False) -> str:
    """Converts Jyutping romanization to Yale romanization.
    Note that the majority of this function and the convertToIPA function
    is derivative of Wiktionary's conversion code, contained in the module
    "yue-pron" (https://en.wiktionary.org/wiki/Module:yue-pron)

    Args:
        jyutping (str): String of valid Jyutping syllables
        use_spaces_to_segment (bool, optional): By default, this function
        attempts to separate Jyutping syllables via valid Jyutping finals.
        When this argument is True, disables Jyutping final detection and
        instead assumes each space-separated string is a valid Jyutping
        syllable. Defaults to False.

    Returns:
        str: String of Yale syllables
    """
    def convert_yale_initial(syllable: str) -> str:
        for expr, repl in YALE_INITIAL_REGEX:
            # Special initials need to be replaced
            if expr.match(syllable):
                return repl

        for initial_len in range(2, 0, -1):
            # Normal initials can just be matched to the predefined list
            # of initials
            curr_string = syllable[:initial_len]
            if curr_string in JYUTPING_INITIALS:
                return curr_string

        return ""

    def convert_yale_final(syllable: str) -> str:
        expr_result = YALE_FINAL_REGEX.search(syllable)
        if not expr_result:
            return syllable

        final = expr_result.group(1)
        tone = int(expr_result.group(2))

        if final in YALE_SPECIAL_FINALS:
            # Some syllables have significant differences compared to Yale
            # Switch them out here
            final = YALE_SPECIAL_FINALS[final]

        if tone in (4, 5, 6):
            # Insert an "h" before the last consonant cluster for light tones
            # as they are indicated in Yale
            final = YALE_LIGHT_TONE_REGEX.sub(r"h\1", final + str(tone))

        # Find first vowel and convert it to display the tone
        for vowel in ("a", "e", "i", "o", "u"):
            vowel_idx = final.find(vowel)
            if vowel_idx != -1:
                final = (f"{final[:vowel_idx]}"
                         f"{YALE_VOWEL_REPLACEMENTS[vowel][tone - 1]}"
                         f"{final[vowel_idx + 1:]}")
                break

        return final

    res = []

    if not jyutping:
        return jyutping

    if use_spaces_to_segment:
        new_jyutping = ""
        for c in jyutping:
            new_jyutping += f" {c} " if c in SPECIAL_CHARACTERS else c
        syllables = new_jyutping.split()
    else:
        syllables = segment_jyutping(
            jyutping, remove_special_characters=False,
            remove_glob_characters=False)

    for syllable in syllables:
        if (len(syllable) == 1) or (syllable in SPECIAL_CHARACTERS):
            # Most numbers, single characters, etc are not Jyutping
            res.append(syllable)
            continue

        # If there is no tone, the syllable cannot be converted to Yale
        tone = -1
        for jyutping_tone in JYUTPING_TONES:
            if syllable.find(str(jyutping_tone)) != -1:
                tone = jyutping_tone
                break
        if tone == -1:
            res.append(syllable)
            continue

        syllable_without_tone = syllable[:-1]
        if syllable_without_tone in YALE_SPECIAL_SYLLABLES:
            # If the Jyutping matches a special syllable, use the corresponding
            # item from the predefined dictionary
            res.append(YALE_SPECIAL_SYLLABLES[syllable_without_tone][tone - 1])
            continue

        yale_initial = convert_yale_initial(syllable)
        yale_final = convert_yale_final(syllable)
        res.append(f"{yale_initial}{yale_final}")

    return " ".join(res)


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


def segment_jyutping(jyutping: str, remove_special_characters: bool = True,
                     remove_glob_characters: bool = True) -> list[str]:
    """Segments Jyutping by looking at valid Jyutping initials and finals.
    Can be configured to remove special characters and/or
    wildcard delimiter (glob) characters.

    Args:
        jyutping (str): String of valid Jyutping syllables, possibly with
            special characters or glob characters
        removeSpecialCharacters (bool, optional): Do not include special
            characters in output list. Defaults to True.
        removeGlobCharacters (bool, optional): Do not include glob characters
            in output list. Defaults to True.

    Returns:
        list[str]: List where each string is a valid Jyutping syllable,
            special character, or glob character
    """
    jyutping = jyutping.lower()
    start_idx, end_idx, initial_found = 0, 0, False
    res = []

    while end_idx < len(jyutping):
        component_found = False

        curr_string = jyutping[end_idx]
        is_special_character = curr_string in SPECIAL_CHARACTERS
        is_glob_character = (curr_string.strip() == "*"
                             or curr_string.strip() == "?")

        if (curr_string == " " or curr_string == "'"
                or is_special_character or is_glob_character):
            if initial_found:
                # Whitespace, apostrophes, special characters, and glob
                # characters mean that we *must* split a syllable
                syllable = jyutping[start_idx:end_idx]
                res.append(syllable)
                start_idx = end_idx
                initial_found = False

            if not remove_glob_characters and is_glob_character:
                # Whitespace matters for glob characters! Consume
                # the next or previous whitespace if it exists and the
                # whitespace was not consumed by another syllable
                glob_start_idx = end_idx
                glob_end_idx = glob_start_idx + 1

                if ((end_idx >= 1) and (jyutping[end_idx - 1] == " ")
                        and (res and res[-1][-1] != " ")):
                    # Keep whitespace preceding the glob character ONLY IF
                    # whitespace was not already added to the previous syllable
                    glob_start_idx -= 1
                if ((len(jyutping) > (end_idx + 1))
                        and (jyutping[end_idx + 1] == " ")):
                    # If there is whitespace succeeding the glob character,
                    # add it to this syllable, and mark the whitespace as
                    # being consumed by incrementing end_idx
                    glob_end_idx += 1
                    end_idx += 1

                glob_str = jyutping[glob_start_idx:glob_end_idx]
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
                initial = jyutping[start_idx:end_idx]
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
            curr_string = jyutping[end_idx:end_idx+initial_len]

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
                first_initial = jyutping[start_idx:end_idx]
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
            curr_string = jyutping[end_idx:end_idx+final_len]
            if curr_string in JYUTPING_FINALS:
                end_idx += final_len
                if end_idx < len(jyutping):
                    if jyutping[end_idx].isnumeric():
                        # Append the tone digit following the final to the
                        # syllable
                        end_idx += 1
                syllable = jyutping[start_idx:end_idx]
                res.append(syllable)
                start_idx = end_idx
                component_found = True
                initial_found = False
                break

        if component_found:
            continue

        end_idx += 1

    # Add whatever's left in the search term, minus whitespace
    last_word = jyutping[start_idx:]
    last_word = ' '.join(last_word.split())
    last_word = last_word.strip()
    if last_word and last_word != "'":
        res.append(last_word)

    return res


def segment_pinyin(pinyin: str, remove_special_characters: bool = True,
                   remove_glob_characters: bool = True) -> list[str]:
    """Segments Pinyin by looking at valid Pinyin initials and finals.
    Can be configured to remove special characters and/or
    wildcard delimiter (glob) characters.

    Args:
        pinyin (str): String of valid Pinyin syllables, possibly with special
            characters or glob characters
        removeSpecialCharacters (bool, optional): Do not include special
            characters in output list. Defaults to True.
        removeGlobCharacters (bool, optional): Do not include glob characters
            in output list. Defaults to True.

    Returns:
        list[str]: List where each string is a valid Pinyin syllable, special
            character, or glob character
    """
    pinyin = pinyin.lower()
    start_idx, end_idx, initial_found = 0, 0, False
    res = []

    while end_idx < len(pinyin):
        component_found = False

        curr_string = pinyin[end_idx]
        is_special_character = curr_string in SPECIAL_CHARACTERS
        is_glob_character = (curr_string.strip() == "*"
                             or curr_string.strip() == "?")

        if (curr_string == " " or curr_string == "'"
                or is_special_character or is_glob_character):
            if initial_found:
                # Whitespace, apostrophes, special characters, and glob
                # characters mean that we *must* split a syllable
                syllable = pinyin[start_idx:end_idx]
                res.append(syllable)
                start_idx = end_idx
                initial_found = False

            if not remove_glob_characters and is_glob_character:
                # Whitespace matters for glob characters! Consume
                # the next or previous whitespace if it exists and the
                # whitespace was not consumed by another syllable
                glob_start_idx = end_idx
                glob_end_idx = glob_start_idx + 1

                if ((end_idx >= 1) and (pinyin[end_idx - 1] == " ")
                        and (res and res[-1][-1] != " ")):
                    # Keep whitespace preceding the glob character ONLY IF
                    # whitespace was not already added to the previous syllable
                    glob_start_idx -= 1
                if ((len(pinyin) > (end_idx + 1))
                        and (pinyin[end_idx + 1] == " ")):
                    # If there is whitespace succeeding the glob character,
                    # add it to this syllable, and mark the whitespace as
                    # being consumed by incrementing end_idx
                    glob_end_idx += 1
                    end_idx += 1

                glob_str = pinyin[glob_start_idx:glob_end_idx]
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
            curr_string = pinyin[end_idx:end_idx+initial_len]
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
            curr_string = pinyin[end_idx:end_idx+final_len]
            if curr_string in PINYIN_FINALS:
                end_idx += final_len
                if end_idx < len(pinyin):
                    if pinyin[end_idx].isnumeric():
                        # Append the tone digit following the final to the
                        # syllable
                        end_idx += 1
                syllable = pinyin[start_idx:end_idx]
                res.append(syllable)
                start_idx = end_idx
                component_found = True
                initial_found = False
                break

        if component_found:
            continue

        end_idx += 1

    # Add whatever's left in the search term, minus whitespace
    last_word = pinyin[start_idx:]
    last_word = ' '.join(last_word.split())
    last_word = last_word.strip()
    if last_word and last_word != "'":
        res.append(last_word)

    return res
