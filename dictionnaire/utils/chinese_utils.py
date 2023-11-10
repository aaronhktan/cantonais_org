import re
from unicodedata import normalize

SPECIAL_CHARACTERS = (".", "。", ",", "，", "!",  "！", "?", "？", "%",  "－",
                      "…", "⋯",  ".", "·",  "\"", "“",  "”", "$",  "｜",)

JYUTPING_INITIALS = ("b",  "p", "m",  "f",  "d",
                     "t",  "n", "l",  "g",  "k",
                     "ng", "h", "gw", "kw", "w",
                     "z",  "c", "s",  "j",  "m")

JYUTPING_FINALS = ("a",   "aa",  "aai", "aau",  "aam", "aan", "aang", "aap",
                   "aat", "aak", "ai",  "au",   "am",  "an",  "ang",  "ap",
                   "at",  "ak",  "e",   "ei",   "eu",  "em",  "en",   "eng",
                   "ep",  "ek",  "i",   "iu",   "im",  "in",  "ing",  "ip",
                   "it",  "ik",  "o",   "oi",   "ou",  "on",  "ong",  "ot",
                   "ok",  "u",   "ui",  "un",   "ung", "ut",  "uk",   "oe",
                   "oet", "eoi", "eon", "oeng", "eot", "oek", "yu",   "yun",
                   "yut", "m",   "ng")

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

CANTONESE_IPA_REGEX = re.compile(r"([bcdfghjklmnpqrstvwxyz]?"
                                 r"[bcdfghjklmnpqrstvwxyz]"
                                 r"?)([a@e>i|o~u^y][eo]?)"
                                 r"([iuymngptk]?g?)([1-9])")
CANTONESE_IPA_PREPROCESS_INITIAL_REGEX = {
    re.compile(r"([zcs])yu"): r"\1hyu",
    re.compile(r"([zc])oe"): r"\1hoe",
    re.compile(r"([zc])eo"): r"\1heo",
}
CANTONESE_IPA_SPECIAL_SYLLABLE_REGEX = re.compile(r"^(h?)([mn]g?)([1-6])$")
CANTONESE_IPA_TONE_REGEX = re.compile("[1-6]")
CANTONESE_IPA_CHECKED_TONES_REGEX = re.compile("([ptk])([136])")

CANTONESE_IPA_SPECIAL_FINALS = {
    "a": "@",
    "yu": "y",
    "@@": "a",
    "uk": "^k",
    "ik": "|k",
    "ou": "~u",
    "eoi": "eoy",
    "ung": "^ng",
    "ing": "|ng",
    "ei": ">i",
}

CANTONESE_IPA_INITIALS = {
    "b": "p",
    "p": "pʰ",
    "d": "t",
    "t": "tʰ",
    "g": "k",
    "k": "kʰ",
    "ng": "ŋ",
    "gw": "kʷ",
    "kw": "kʷʰ",
    "zh": "t͡ʃ",
    "ch": "t͡ʃʰ",
    "sh": "ʃ",
    "z": "t͡s",
    "c": "t͡sʰ",
}

CANTONESE_IPA_NUCLEI = {
    "a": "äː",
    "@": "ɐ",
    "e": "ɛː",
    ">": "e",
    "i": "iː",
    "|": "ɪ",
    "o": "ɔː",
    "~": "o",
    "oe": "œ̽ː",
    "eo": "ɵ",
    "u": "uː",
    "^": "ʊ",
    "y": "yː",
}

CANTONESE_IPA_CODAS = {
    "i": "i̯",
    "u": "u̯",
    "y": "y̯",
    "ng": "ŋ",
    "p": "p̚",
    "t": "t̚",
    "k": "k̚",
}

CANTONESE_IPA_TONES = ("˥", "˧˥", "˧", "˨˩", "˩˧", "˨", "˥", "˧", "˨")

PINYIN_INITIALS = ("b", "p", "m",  "f",  "d",  "t",
                   "n", "l", "g",  "k",  "h",  "j",
                   "q", "x", "zh", "ch", "sh", "r",
                   "z", "c", "s")

PINYIN_FINALS = ("a",   "e",   "ai",  "ei",  "ao",   "ou",  "an",   "ang",
                 "en",  "ang", "eng", "ong", "er",   "i",   "ia",   "ie",
                 "iao", "iu",  "ian", "in",  "iang", "ing", "iong", "u",
                 "ua",  "uo",  "uai", "ui",  "uan",  "un",  "uang", "u",
                 "u:",  "ue",  "u:e", "o")

PINYIN_TONES = (1, 2, 3, 4, 5)

PINYIN_PRIORITY_DIACRITIC = ("a", "e", "o")
PINYIN_SECONDARY_DIACRITIC = ("i", "u", "ü")

PINYIN_TONE_REPLACEMENTS = {
    "a": ("ā", "á", "ǎ", "à", "a"),
    "e": ("ē", "é", "ě", "è", "e"),
    "i": ("ī", "í", "ǐ", "ì", "i"),
    "o": ("ō", "ó", "ǒ", "ò", "o"),
    "u": ("ū", "ú", "ǔ", "ù", "u"),
    "ü": ("ǖ", "ǘ", "ǚ", "ǜ", "ü"),
}

ZHUYIN_PREPROCESS_INITIAL_REGEX = {
    re.compile(r"([jqx])u"): r"\1v",
    re.compile(r"([zcs]h?)i"): r"\1",
    re.compile(r"([r])i"): r"\1",
}
ZHUYIN_PREPROCESS_FINAL_REGEX = {
    re.compile(r"^ng([012345])$"): r"ㄫ\1",
    re.compile(r"^hm([012345])$"): r"ㄏㄇ\1",
    re.compile(r"^hng([012345])$"): r"ㄏㄫ\1",
    re.compile(r"^er([012345])$"): r"ㄦ\1",
}
ZHUYIN_INITIAL_REGEX = re.compile(r"^([bpmfdtnlgkhjqxzcsr]?h?)")
ZHUYIN_FINAL_REGEX = re.compile(
    r"([aeiouêvyw]?[aeioun]?[aeioung]?[ng]?)(r?)([012345])$")

ZHUYIN_INITIALS = {
    "b": "ㄅ",  "p": "ㄆ", "m": "ㄇ", "f": "ㄈ",  "d": "ㄉ",
    "t": "ㄊ",  "n": "ㄋ", "l": "ㄌ", "g": "ㄍ",  "k": "ㄎ",
    "h": "ㄏ",  "j": "ㄐ", "q": "ㄑ", "x": "ㄒ",  "z": "ㄗ",
    "c": "ㄘ",  "s": "ㄙ", "r": "ㄖ", "zh": "ㄓ", "ch": "ㄔ",
    "sh": "ㄕ",
}

ZHUYIN_FINALS = {
    "yuan": "ㄩㄢ", "iang": "ㄧㄤ", "yang": "ㄧㄤ", "uang": "ㄨㄤ",
    "wang": "ㄨㄤ", "ying": "ㄧㄥ", "weng": "ㄨㄥ", "iong": "ㄩㄥ",
    "yong": "ㄩㄥ", "uai": "ㄨㄞ",  "wai": "ㄨㄞ",  "yai": "ㄧㄞ",
    "iao": "ㄧㄠ",  "yao": "ㄧㄠ",  "ian": "ㄧㄢ",  "yan": "ㄧㄢ",
    "uan": "ㄨㄢ",  "wan": "ㄨㄢ",  "van": "ㄩㄢ",  "ang": "ㄤ",
    "yue": "ㄩㄝ",  "wei": "ㄨㄟ",  "you": "ㄧㄡ",  "yin": "ㄧㄣ",
    "wen": "ㄨㄣ",  "yun": "ㄩㄣ",  "eng": "ㄥ",   "ing": "ㄧㄥ",
    "ong": "ㄨㄥ",  "io": "ㄧㄛ",   "yo": "ㄧㄛ",   "ia": "ㄧㄚ",
    "ya": "ㄧㄚ",   "ua": "ㄨㄚ",   "wa": "ㄨㄚ",   "ai": "ㄞ",
    "ao": "ㄠ",    "an": "ㄢ",    "ie": "ㄧㄝ",   "ye": "ㄧㄝ",
    "uo": "ㄨㄛ",   "wo": "ㄨㄛ",   "ue": "ㄩㄝ",   "ve": "ㄩㄝ",
    "ei": "ㄟ",    "ui": "ㄨㄟ",   "ou": "ㄡ",     "iu": "ㄧㄡ",
    "en": "ㄣ",    "in": "ㄧㄣ",   "un": "ㄨㄣ",   "vn": "ㄩㄣ",
    "yi": "ㄧ",    "wu": "ㄨ",    "yu": "ㄩ",    "a": "ㄚ",
    "e": "ㄜ",     "o": "ㄛ",     "i": "ㄧ",     "u": "ㄨ",
    "v": "ㄩ",     "ê": "ㄝ",
}
ZHUYIN_TONES = ("", "", "ˊ", "ˇ", "ˋ", "˙")

MANDARIN_IPA_SYLLABLE_REGEX = re.compile(r"^([bcdfghjklmnpqrstxz]?h?)(.+)$")
MANDARIN_CLOSE_FRONT_ROUNDED_VOWEL_REGEX = re.compile(r"([jqx])u")

MANDARIN_IPA_GLOTTAL = ("a", "o", "e", "ai", "ei", "ao",
                        "ou", "an", "en", "er", "ang", "ong", "eng")

MANDARIN_IPA_INITIALS = {
    "b": "p",   "c": "t͡sʰ", "ch": "ʈ͡ʂʰ", "d": "t",  "f": "f",
    "g": "k",   "h": "x",    "j": "t͡ɕ",   "k": "kʰ", "l": "l",
    "m": "m",   "n": "n",    "ng": "ŋ",    "p": "pʰ", "q": "t͡ɕʰ",
    "r": "ʐ",   "s": "s",    "sh": "ʂ",    "t": "tʰ", "x": "ɕ",
    "z": "t͡s", "zh": "ʈ͡ʂ",
}

MANDARIN_IPA_VOICELESS_INITIALS = {
    "k": "g̊",
    "p": "b̥",
    "t": "d̥",
    "t͡s": "d͡z̥",
    "t͡ɕ": "d͡ʑ̥",
    "ʈ͡ʂ": "ɖ͡ʐ̥",
}

MANDARIN_IPA_FINALS = {
    "a": "ä",       "ai": "aɪ̯",      "air": "ɑɻ",     "an": "än",
    "ang": "ɑŋ",    "angr": "ɑ̃ɻ",    "anr": "ɑɻ",     "ao": "ɑʊ̯",
    "aor": "aʊ̯ɻʷ",  "ar": "ɑɻ",      "e": "ɤ",        "ei": "eɪ̯",
    "eir": "əɻ",    "en": "ən",      "eng": "ɤŋ",     "engr": "ɤ̃ɻ",
    "enr": "ʊ̃ɻ",    "er": "ɤɻ",      "i": "i",        "ia": "jä",
    "ian": "jɛn",   "iang": "jɑŋ",   "iangr": "jɑ̃ɻ",  "ianr": "jɑɻ",
    "iao": "jɑʊ̯",   "iaor": "jaʊ̯ɻʷ", "iar": "jɑɻ",    "ie": "jɛ",
    "ier": "jɛɻ",   "in": "in",      "ing": "iŋ",     "ingr": "iɤ̯̃ɻ",
    "inr": "iə̯ɻ",   "io": "jɔ",      "iong": "jʊŋ",   "iongr": "jʊ̃ɻ",
    "ir": "iə̯ɻ",    "iu": "joʊ̯",     "iur": "jɤʊ̯ɻʷ",  "m": "m̩",
    "n": "n̩",       "ng": "ŋ̍",       "o": "wɔ",       "ong": "ʊŋ",
    "ongr": "ʊ̃ɻ",   "or": "wɔɻ",     "ou": "oʊ̯",      "our": "ɤʊ̯ɻʷ",
    "u": "u",       "ua": "u̯ä",      "uai": "waɪ̯",    "uair": "wɑɻ",
    "uan": "wän",   "uang": "wɑŋ",   "uangr": "wɑ̃ɻ",  "uanr": "wɑɻ",
    "uar": "u̯ɑɻ",   "ue": "ɥɛ",      "ui": "weɪ̯",     "uir": "wəɻ",
    "un": "wən",    "unr": "wəɻ",    "uo": "wɔ",      "uor": "wɔɻ",
    "ur": "uɻʷ",    "v": "y",        "van": "ɥɛn",    "vanr": "ɥɑɻ",
    "ve": "ɥɛ",     "ver": "ɥɛɻ",    "vn": "yn",      "vnr": "yə̯ɻ",
    "vr": "yə̯ɻ",    "wa": "wä",      "wai": "waɪ̯",    "wair": "wɑɻ",
    "wan": "wän",   "wang": "wɑŋ",   "wangr": "wɑ̃ɻ",  "wanr": "wɑɻ",
    "war": "wɑɻ",   "wei": "weɪ̯",    "weir": "wəɻ",   "wen": "wən",
    "weng": "wəŋ",  "wengr": "ʊ̃ɻ",   "wenr": "wəɻ",   "wo": "wɔ",
    "wor": "wɔɻ",   "wu": "u",       "wur": "uɻʷ",    "ya": "jä",
    "yai": "jaɪ̯",   "yan": "jɛn",    "yang": "jɑŋ",   "yangr": "jɑ̃ɻ",
    "yanr": "jɑɻ",  "yao": "jɑʊ̯",    "yaor": "jaʊ̯ɻʷ", "yar": "jɑɻ",
    "ye": "jɛ",     "yer": "jɛɻ",    "yi": "i",       "yin": "in",
    "ying": "iŋ",   "yingr": "iɤ̯̃ɻ",  "yinr": "iə̯ɻ",   "yir": "iə̯ɻ",
    "yo": "jɔ",     "yong": "jʊŋ",   "yongr": "jʊ̃ɻ",  "yor": "jɔɻ",
    "you": "joʊ̯",   "your": "jɤʊ̯ɻʷ", "yu": "y",       "yuan": "ɥɛn",
    "yuanr": "ɥɑɻ", "yue": "ɥɛ",     "yuer": "ɥɛɻ",   "yun": "yn",
    "yunr": "yə̯ɻ",  "yur": "yə̯ɻ",
}

MANDARIN_IPA_NEUTRAL_TONE = ("˨", "˧", "˦", "˩", "˩")

MANDARIN_IPA_THIRD_TONE = ("˨˩˦꜕꜖꜖", "˨˩˦꜕꜖꜖", "˨˩˦꜔꜒", "˨˩˦꜕꜖꜖", "˨˩˦")

MANDARIN_IPA_TONES = ("˥˥", "˧˥", "˨˩˦", "˥˩", "")

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
        try:
            if c.isnumeric() and int(c) in JYUTPING_TONES:
                res.append(int(c))
        except:
            pass
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
        try:
            if c.isnumeric() and int(c) in PINYIN_TONES:
                res.append(int(c))
        except:
            pass
    return res


def apply_colours(original: str, tones: list[int],
                  tone_colours: list[str]) -> str:
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


def jyutping_to_IPA(jyutping: str, use_spaces_to_segment: bool = False) -> str:
    """Converts Jyutping romanization to Cantonese Sinological IPA

    Args:
        jyutping (str): String of valid Jyutping syllables
        use_spaces_to_segment (bool, optional): By default, this function
        attempts to separate Jyutping syllables via valid Jyutping finals.
        When this argument is True, disables Jyutping final detection and
        instead assumes each space-separated string is a valid Jyutping
        syllable. Defaults to False.

    Returns:
        str: String of Cantonese Sinological IPA syllables
    """
    def convert_ipa_syllable(syllable):
        initial = ""
        nucleus = ""
        coda = ""
        tone = ""

        match = CANTONESE_IPA_REGEX.match(syllable)
        if not match:
            return syllable

        if match.group(1):
            if match.group(1) in CANTONESE_IPA_INITIALS:
                initial = CANTONESE_IPA_INITIALS[match.group(1)]
            else:
                initial = match.group(1)

        if match.group(2):
            if match.group(2) in CANTONESE_IPA_NUCLEI:
                nucleus = CANTONESE_IPA_NUCLEI[match.group(2)]
            else:
                nucleus = match[2]

        if match.group(3):
            if match.group(3) in CANTONESE_IPA_CODAS:
                coda = CANTONESE_IPA_CODAS[match.group(3)]
            else:
                coda = match.group(3)

        if match.group(4):
            tone = CANTONESE_IPA_TONES[int(match.group(4)) - 1]

        return f"{initial}{nucleus}{coda}{tone}"

    res = []

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

        # If there is no tone, the syllable cannot be converted to IPA
        tone = -1
        for jyutping_tone in JYUTPING_TONES:
            if syllable.find(str(jyutping_tone)) != -1:
                tone = jyutping_tone
                break
        if tone == -1:
            res.append(syllable)
            continue

        # Do some pre-processing for initials
        for pattern, repl in CANTONESE_IPA_PREPROCESS_INITIAL_REGEX.items():
            syllable = pattern.sub(repl, syllable)

        # Convert special syllables
        match = CANTONESE_IPA_SPECIAL_SYLLABLE_REGEX.match(syllable)
        if match:
            syllable = syllable.replace("m", "m̩")
            syllable = syllable.replace("ng", "ŋ̍")
            syllable = CANTONESE_IPA_TONE_REGEX.sub(
                CANTONESE_IPA_TONES[tone - 1], syllable)

        # Replace checked tones
        match = CANTONESE_IPA_CHECKED_TONES_REGEX.search(syllable)
        if match:
            syllable = syllable.replace("1", "7")
            syllable = syllable.replace("3", "8")
            syllable = syllable.replace("6", "9")

        # More preprocessing
        for spec, repl in CANTONESE_IPA_SPECIAL_FINALS.items():
            syllable = syllable.replace(spec, repl)

        res.append(convert_ipa_syllable(syllable))

    return " ".join(res)


def pretty_pinyin(pinyin: str) -> str:
    """Converts raw Pinyin in database (with u: and digits for tones)
    to the conventional Hanyu Pinyin representation

    Args:
        pinyin (str): String of valid raw Pinyin syllables

    Returns:
        str: String of pretty Pinyin syllables
    """
    if not pinyin:
        return pinyin

    syllables = pinyin.split()
    if not syllables:
        return pinyin

    res = []

    for syllable in syllables:
        if (len(syllable) == 1) or (syllable in SPECIAL_CHARACTERS):
            # Most numbers, single characters, etc are not Pinyin
            res.append(syllable)
            continue

        # If there is no tone, the syllable cannot be converted
        tone = -1
        for pinyin_tone in PINYIN_TONES:
            if syllable.find(str(pinyin_tone)) != -1:
                tone = pinyin_tone
                break
        if tone == -1:
            res.append(syllable)
            continue

        syllable = syllable.replace("u:", "ü")

        # In Pinyin, the diacritic is always placed over the first
        # A, E, or O if they exist.
        diacritic_vowel_idx = float("inf")
        diacritic_vowel = None
        for priority_vowel in PINYIN_PRIORITY_DIACRITIC:
            idx = syllable.find(priority_vowel)
            if idx != -1 and idx < diacritic_vowel_idx:
                diacritic_vowel_idx = idx
                diacritic_vowel = priority_vowel
        # Otherwise, the diacritic goes on the last U or I
        if not diacritic_vowel:
            diacritic_vowel_idx = float("-inf")
            for secondary_vowel in PINYIN_SECONDARY_DIACRITIC:
                idx = syllable.find(secondary_vowel)
                if idx != -1 and idx > diacritic_vowel_idx:
                    diacritic_vowel_idx = idx
                    diacritic_vowel = secondary_vowel
        if not diacritic_vowel:
            # No vowel to put an accent on was found :(
            res.append(syllable)
            continue

        # Add the diacritic
        syllable = syllable.replace(
            diacritic_vowel,
            PINYIN_TONE_REPLACEMENTS[diacritic_vowel][tone - 1],
            1)

        # Remove the tone
        syllable = syllable[:-1]
        res.append(syllable)

    return " ".join(res)


def numbered_pinyin(pinyin: str) -> str:
    """Converts raw Pinyin in database (with u:) to representation
    using the ü but retaining digits for tones

    Args:
        pinyin (str): String of valid raw Pinyin syllables

    Returns:
        str: String of numbered Pinyin syllables with ü
    """
    if not pinyin:
        return pinyin

    return pinyin.replace("u:", "ü")


def pinyin_with_v(pinyin: str) -> str:
    """Converts raw Pinyin in database (with u:) to representation
    using "v" to represent "ü" but retaining digits for tones.

    Args:
        pinyin (str): String of valid raw Pinyin syllables

    Returns:
        str: String of numbered Pinyin syllables with v
    """
    if not pinyin:
        return pinyin

    return pinyin.replace("u:", "v")


def pinyin_to_zhuyin(pinyin: str, use_spaces_to_segment: bool = False) -> str:
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
    if not pinyin:
        return pinyin

    res = []

    if use_spaces_to_segment:
        syllables = pinyin.split()
    else:
        syllables = segment_pinyin(pinyin)

    for syllable in syllables:
        if (len(syllable) == 1) or (syllable in SPECIAL_CHARACTERS):
            # Most numbers, single characters, etc are not Pinyin
            res.append(syllable)
            continue

        # If there is no tone, the syllable cannot be converted to Zhuyin
        tone = -1
        for pinyin_tone in PINYIN_TONES:
            if syllable.find(str(pinyin_tone)) != -1:
                tone = pinyin_tone
                break
        if tone == -1:
            res.append(syllable)
            continue

        syllable = pinyin_with_v(syllable)

        # Handle some special cases for Zhuyin
        for pattern, repl in ZHUYIN_PREPROCESS_INITIAL_REGEX.items():
            syllable = pattern.sub(repl, syllable)
        for pattern, repl in ZHUYIN_PREPROCESS_FINAL_REGEX.items():
            syllable = pattern.sub(repl, syllable)

        # Handle general case
        match = ZHUYIN_INITIAL_REGEX.search(syllable)
        if match:
            if match.group(1):
                syllable = ZHUYIN_INITIAL_REGEX.sub(
                    ZHUYIN_INITIALS[match.group(1)], syllable)

        match = ZHUYIN_FINAL_REGEX.search(syllable)
        if match:
            final, er = "", ""
            if match.group(1):
                if match.group(1) not in ZHUYIN_FINALS:
                    # Failed to match final, give up
                    res.append(syllable)
                    continue
                final = ZHUYIN_FINALS[match.group(1)]
            if match.group(2):
                er = "ㄦ"
            syllable = ZHUYIN_FINAL_REGEX.sub(final + er, syllable)

        er_idx = syllable.find("ㄦ")
        if tone == 5:
            syllable = ZHUYIN_TONES[tone] + syllable
        elif er_idx != -1 and syllable != "ㄦ":
            syllable = syllable[:er_idx] + \
                ZHUYIN_TONES[tone] + syllable[er_idx:]
        else:
            syllable = syllable + ZHUYIN_TONES[tone]

        res.append(syllable)

    return " ".join(res)


def pinyin_to_IPA(pinyin: str, use_spaces_to_segment: bool = False) -> str:
    """Convert raw Pinyin in database to Mandarin Sinological IPA.

    Args:
        pinyin (str): String of valid raw Pinyin syllables
        use_spaces_to_segment (bool, optional): By default, this function
        attempts to separate Pinyin syllables via valid Pinyin finals.
        When this argument is True, disables Pinyin final detection and
        instead assumes each space-separated string is a valid Pinyin
        syllable. Defaults to False.

    Returns:
        str: String of Mandarin Sinological IPA syllables
    """

    def convert_ipa_syllable(syllable):
        initial, final = "", ""
        if syllable == "ng":
            final = MANDARIN_IPA_FINALS[syllable]
        else:
            match = MANDARIN_IPA_SYLLABLE_REGEX.match(syllable)
            if not match:
                return syllable

            conversion_failure = False
            if match.group(1):
                if match.group(1) not in MANDARIN_IPA_INITIALS:
                    conversion_failure = True
                else:
                    initial = MANDARIN_IPA_INITIALS[match.group(1)]
            if match.group(2):
                if match.group(2) not in MANDARIN_IPA_FINALS:
                    conversion_failure = True
                else:
                    final = MANDARIN_IPA_FINALS[match.group(2)]
            
            # Exit early if any initial or final could not be converted
            if conversion_failure:
                return match.group(1), match.group(2)

        # Replace close front unrounded vowel with syllable retroflex sibilant
        # fricative (+ voiced retroflex approximant if erhua) in Pinyin
        # starting with ch, sh, zh, or r
        if initial in ("ʈ͡ʂʰ", "ʂ", "ʈ͡ʂ", "ʐ"):
            if final == "ir":
                final = "ʐ̩ɻ"
            elif final == "i":
                final = "ʐ̩"

        # Replace close front unrounded vowel with syllablic alveolar sibilant
        # fricative (+ voiced retroflex approximant if erhua) in Pinyin
        # starting with c, s, or z
        if initial in ("t͡sʰ", "s", "t͡s"):
            if final == "ir":
                final = "z̩ɻ"
            elif final == "i":
                final = "z̩̩"

        if initial == "ʐ" and final == "ʐ̩":
            initial = ""

        return initial, final

    if not pinyin:
        return pinyin

    if use_spaces_to_segment:
        syllables = pinyin.split()
    else:
        syllables = segment_pinyin(pinyin)

    # Precompute list of tones corresponding to each syllable
    # This list is later used for tone sandhi reasons
    # (e.g. 3->3 sandhi, x->5 sandhi, etc.)
    syllable_tones = []
    for syllable in syllables:
        syllable_tone = -1
        for pinyin_tone in PINYIN_TONES:
            syllable_tone_idx = syllable.find(str(pinyin_tone))
            if syllable_tone_idx != -1:
                syllable_tone = pinyin_tone
                syllable_tones.append((pinyin_tone, syllable_tone_idx))
                break
        if syllable_tone == -1:
            syllable_tones.append((-1, -1))

    res = []

    for syllable_idx, syllable in enumerate(syllables):
        glottal, initial, final, tone = "", "", "", ""

        if (len(syllable) == 1) or (syllable in SPECIAL_CHARACTERS):
            # Most numbers, single characters, etc are not Pinyin
            res.append(syllable)
            continue

        syllable_tone, syllable_tone_idx = syllable_tones[syllable_idx]
        if syllable_tone_idx == -1:
            # If there is no tone, the syllable cannot be converted to Zhuyin
            res.append(syllable)
            continue

        # Figure out whether this syllable needs a glottal stop
        syllable_without_tone = syllable[:syllable_tone_idx] + \
            syllable[syllable_tone_idx+1:]
        if syllable_without_tone in MANDARIN_IPA_GLOTTAL:
            glottal = "ˀ"

        # Mark close front rounded vowel with v instead of "u"
        syllable_without_tone = syllable_without_tone.replace("u:", "v")
        syllable_without_tone = MANDARIN_CLOSE_FRONT_ROUNDED_VOWEL_REGEX.sub(
            r"\1v", syllable_without_tone)

        # Convert main part of the Mandarin syllable
        initial, final = convert_ipa_syllable(syllable_without_tone)

        # Convert tone
        if syllable_idx + 1 < len(syllables):
            next_tone = syllable_tones[syllable_idx + 1][0]
        else:
            next_tone = "-1"

        if syllable_idx > 0:
            prev_tone = syllable_tones[syllable_idx - 1][0]
        else:
            prev_tone = "-1"

        match int(syllable_tone):
            case 5:
                # When neutral tone, some initials must be replaced with
                # their voiceless versions
                if initial in MANDARIN_IPA_VOICELESS_INITIALS:
                    initial = MANDARIN_IPA_VOICELESS_INITIALS[initial]
                if final == "ɤ":
                    final = "ə"
                tone = "" if prev_tone == "-1" else MANDARIN_IPA_NEUTRAL_TONE[prev_tone - 1]
            case 3:
                if syllable_idx == len(syllables) - 1:
                    # Last syllable with tone 3 can drop the rising part
                    # of the tone
                    tone = "˨˩˦" if syllable_idx == 0 else "˨˩˦꜕꜖(꜓)"
                else:
                    # If the next syllable doesn't have a tone, default to
                    # no tone sandhi (which is also what happens when the
                    # next tone is tone 5)
                    tone = MANDARIN_IPA_THIRD_TONE[4] if next_tone == - \
                        1 else MANDARIN_IPA_THIRD_TONE[next_tone - 1]
            case 4:
                if next_tone == 4:
                    tone = "˥˩꜒꜔"
                else:
                    tone = MANDARIN_IPA_TONES[syllable_tone - 1]
            case _:
                tone = MANDARIN_IPA_TONES[syllable_tone - 1]

        res.append(normalize(
            "NFC", glottal + initial + final + tone))

    return " ".join(res)


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
                if end_idx < len(pinyin) and pinyin[end_idx] == "r":
                    # Append erhua to syllable if present
                    end_idx += 1

                if end_idx < len(pinyin) and pinyin[end_idx].isnumeric():
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
