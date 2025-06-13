import re
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

PINYIN_INITIALS = (
    "b",
    "p",
    "m",
    "f",
    "d",
    "t",
    "n",
    "l",
    "g",
    "k",
    "h",
    "j",
    "q",
    "x",
    "zh",
    "ch",
    "sh",
    "r",
    "z",
    "c",
    "s",
)

PINYIN_FINALS = (
    "a",
    "e",
    "ai",
    "ei",
    "ao",
    "ou",
    "an",
    "ang",
    "en",
    "ang",
    "eng",
    "ong",
    "er",
    "i",
    "ia",
    "ie",
    "iao",
    "iu",
    "ian",
    "in",
    "iang",
    "ing",
    "iong",
    "u",
    "ua",
    "uo",
    "uai",
    "ui",
    "uan",
    "un",
    "uang",
    "u",
    "u:",
    "ue",
    "u:e",
    "o",
)

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
    r"([aeiouêvyw]?[aeioun]?[aeioung]?[ng]?)(r?)([012345])$"
)

ZHUYIN_INITIALS = {
    "b": "ㄅ",
    "p": "ㄆ",
    "m": "ㄇ",
    "f": "ㄈ",
    "d": "ㄉ",
    "t": "ㄊ",
    "n": "ㄋ",
    "l": "ㄌ",
    "g": "ㄍ",
    "k": "ㄎ",
    "h": "ㄏ",
    "j": "ㄐ",
    "q": "ㄑ",
    "x": "ㄒ",
    "z": "ㄗ",
    "c": "ㄘ",
    "s": "ㄙ",
    "r": "ㄖ",
    "zh": "ㄓ",
    "ch": "ㄔ",
    "sh": "ㄕ",
}

ZHUYIN_FINALS = {
    "yuan": "ㄩㄢ",
    "iang": "ㄧㄤ",
    "yang": "ㄧㄤ",
    "uang": "ㄨㄤ",
    "wang": "ㄨㄤ",
    "ying": "ㄧㄥ",
    "weng": "ㄨㄥ",
    "iong": "ㄩㄥ",
    "yong": "ㄩㄥ",
    "uai": "ㄨㄞ",
    "wai": "ㄨㄞ",
    "yai": "ㄧㄞ",
    "iao": "ㄧㄠ",
    "yao": "ㄧㄠ",
    "ian": "ㄧㄢ",
    "yan": "ㄧㄢ",
    "uan": "ㄨㄢ",
    "wan": "ㄨㄢ",
    "van": "ㄩㄢ",
    "ang": "ㄤ",
    "yue": "ㄩㄝ",
    "wei": "ㄨㄟ",
    "you": "ㄧㄡ",
    "yin": "ㄧㄣ",
    "wen": "ㄨㄣ",
    "yun": "ㄩㄣ",
    "eng": "ㄥ",
    "ing": "ㄧㄥ",
    "ong": "ㄨㄥ",
    "io": "ㄧㄛ",
    "yo": "ㄧㄛ",
    "ia": "ㄧㄚ",
    "ya": "ㄧㄚ",
    "ua": "ㄨㄚ",
    "wa": "ㄨㄚ",
    "ai": "ㄞ",
    "ao": "ㄠ",
    "an": "ㄢ",
    "ie": "ㄧㄝ",
    "ye": "ㄧㄝ",
    "uo": "ㄨㄛ",
    "wo": "ㄨㄛ",
    "ue": "ㄩㄝ",
    "ve": "ㄩㄝ",
    "ei": "ㄟ",
    "ui": "ㄨㄟ",
    "ou": "ㄡ",
    "iu": "ㄧㄡ",
    "en": "ㄣ",
    "in": "ㄧㄣ",
    "un": "ㄨㄣ",
    "vn": "ㄩㄣ",
    "yi": "ㄧ",
    "wu": "ㄨ",
    "yu": "ㄩ",
    "a": "ㄚ",
    "e": "ㄜ",
    "o": "ㄛ",
    "i": "ㄧ",
    "u": "ㄨ",
    "v": "ㄩ",
    "ê": "ㄝ",
}
ZHUYIN_TONES = ("", "", "ˊ", "ˇ", "ˋ", "˙")

MANDARIN_IPA_SYLLABLE_REGEX = re.compile(r"^([bcdfghjklmnpqrstxz]?h?)(.+)$")
MANDARIN_CLOSE_FRONT_ROUNDED_VOWEL_REGEX = re.compile(r"([jqx])u")

MANDARIN_IPA_GLOTTAL = (
    "a",
    "o",
    "e",
    "ai",
    "ei",
    "ao",
    "ou",
    "an",
    "en",
    "er",
    "ang",
    "ong",
    "eng",
)

MANDARIN_IPA_INITIALS = {
    "b": "p",
    "c": "t͡sʰ",
    "ch": "ʈ͡ʂʰ",
    "d": "t",
    "f": "f",
    "g": "k",
    "h": "x",
    "j": "t͡ɕ",
    "k": "kʰ",
    "l": "l",
    "m": "m",
    "n": "n",
    "ng": "ŋ",
    "p": "pʰ",
    "q": "t͡ɕʰ",
    "r": "ʐ",
    "s": "s",
    "sh": "ʂ",
    "t": "tʰ",
    "x": "ɕ",
    "z": "t͡s",
    "zh": "ʈ͡ʂ",
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
    "a": "ä",
    "ai": "aɪ̯",
    "air": "ɑɻ",
    "an": "än",
    "ang": "ɑŋ",
    "angr": "ɑ̃ɻ",
    "anr": "ɑɻ",
    "ao": "ɑʊ̯",
    "aor": "aʊ̯ɻʷ",
    "ar": "ɑɻ",
    "e": "ɤ",
    "ei": "eɪ̯",
    "eir": "əɻ",
    "en": "ən",
    "eng": "ɤŋ",
    "engr": "ɤ̃ɻ",
    "enr": "ʊ̃ɻ",
    "er": "ɤɻ",
    "i": "i",
    "ia": "jä",
    "ian": "jɛn",
    "iang": "jɑŋ",
    "iangr": "jɑ̃ɻ",
    "ianr": "jɑɻ",
    "iao": "jɑʊ̯",
    "iaor": "jaʊ̯ɻʷ",
    "iar": "jɑɻ",
    "ie": "jɛ",
    "ier": "jɛɻ",
    "in": "in",
    "ing": "iŋ",
    "ingr": "iɤ̯̃ɻ",
    "inr": "iə̯ɻ",
    "io": "jɔ",
    "iong": "jʊŋ",
    "iongr": "jʊ̃ɻ",
    "ir": "iə̯ɻ",
    "iu": "joʊ̯",
    "iur": "jɤʊ̯ɻʷ",
    "m": "m̩",
    "n": "n̩",
    "ng": "ŋ̍",
    "o": "wɔ",
    "ong": "ʊŋ",
    "ongr": "ʊ̃ɻ",
    "or": "wɔɻ",
    "ou": "oʊ̯",
    "our": "ɤʊ̯ɻʷ",
    "u": "u",
    "ua": "u̯ä",
    "uai": "waɪ̯",
    "uair": "wɑɻ",
    "uan": "wän",
    "uang": "wɑŋ",
    "uangr": "wɑ̃ɻ",
    "uanr": "wɑɻ",
    "uar": "u̯ɑɻ",
    "ue": "ɥɛ",
    "ui": "weɪ̯",
    "uir": "wəɻ",
    "un": "wən",
    "unr": "wəɻ",
    "uo": "wɔ",
    "uor": "wɔɻ",
    "ur": "uɻʷ",
    "v": "y",
    "van": "ɥɛn",
    "vanr": "ɥɑɻ",
    "ve": "ɥɛ",
    "ver": "ɥɛɻ",
    "vn": "yn",
    "vnr": "yə̯ɻ",
    "vr": "yə̯ɻ",
    "wa": "wä",
    "wai": "waɪ̯",
    "wair": "wɑɻ",
    "wan": "wän",
    "wang": "wɑŋ",
    "wangr": "wɑ̃ɻ",
    "wanr": "wɑɻ",
    "war": "wɑɻ",
    "wei": "weɪ̯",
    "weir": "wəɻ",
    "wen": "wən",
    "weng": "wəŋ",
    "wengr": "ʊ̃ɻ",
    "wenr": "wəɻ",
    "wo": "wɔ",
    "wor": "wɔɻ",
    "wu": "u",
    "wur": "uɻʷ",
    "ya": "jä",
    "yai": "jaɪ̯",
    "yan": "jɛn",
    "yang": "jɑŋ",
    "yangr": "jɑ̃ɻ",
    "yanr": "jɑɻ",
    "yao": "jɑʊ̯",
    "yaor": "jaʊ̯ɻʷ",
    "yar": "jɑɻ",
    "ye": "jɛ",
    "yer": "jɛɻ",
    "yi": "i",
    "yin": "in",
    "ying": "iŋ",
    "yingr": "iɤ̯̃ɻ",
    "yinr": "iə̯ɻ",
    "yir": "iə̯ɻ",
    "yo": "jɔ",
    "yong": "jʊŋ",
    "yongr": "jʊ̃ɻ",
    "yor": "jɔɻ",
    "you": "joʊ̯",
    "your": "jɤʊ̯ɻʷ",
    "yu": "y",
    "yuan": "ɥɛn",
    "yuanr": "ɥɑɻ",
    "yue": "ɥɛ",
    "yuer": "ɥɛɻ",
    "yun": "yn",
    "yunr": "yə̯ɻ",
    "yur": "yə̯ɻ",
}

MANDARIN_IPA_NEUTRAL_TONE = ("˨", "˧", "˦", "˩", "˩")

MANDARIN_IPA_THIRD_TONE = ("˨˩˦꜕꜖꜖", "˨˩˦꜕꜖꜖", "˨˩˦꜔꜒", "˨˩˦꜕꜖꜖", "˨˩˦")

MANDARIN_IPA_TONES = ("˥˥", "˧˥", "˨˩˦", "˥˩", "")


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
            diacritic_vowel, PINYIN_TONE_REPLACEMENTS[diacritic_vowel][tone - 1], 1
        )

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
        _, syllables = segment_pinyin(pinyin)

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
                    ZHUYIN_INITIALS[match.group(1)], syllable
                )

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
            syllable = syllable[:er_idx] + ZHUYIN_TONES[tone] + syllable[er_idx:]
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
        _, syllables = segment_pinyin(pinyin)

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
        syllable_without_tone = (
            syllable[:syllable_tone_idx] + syllable[syllable_tone_idx + 1:]
        )
        if syllable_without_tone in MANDARIN_IPA_GLOTTAL:
            glottal = "ˀ"

        # Mark close front rounded vowel with v instead of "u"
        syllable_without_tone = syllable_without_tone.replace("u:", "v")
        syllable_without_tone = MANDARIN_CLOSE_FRONT_ROUNDED_VOWEL_REGEX.sub(
            r"\1v", syllable_without_tone
        )

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
                tone = (
                    ""
                    if prev_tone == "-1"
                    else MANDARIN_IPA_NEUTRAL_TONE[prev_tone - 1]
                )
            case 3:
                if syllable_idx == len(syllables) - 1:
                    # Last syllable with tone 3 can drop the rising part
                    # of the tone
                    tone = "˨˩˦" if syllable_idx == 0 else "˨˩˦꜕꜖(꜓)"
                else:
                    # If the next syllable doesn't have a tone, default to
                    # no tone sandhi (which is also what happens when the
                    # next tone is tone 5)
                    tone = (
                        MANDARIN_IPA_THIRD_TONE[4]
                        if next_tone == -1
                        else MANDARIN_IPA_THIRD_TONE[next_tone - 1]
                    )
            case 4:
                if next_tone == 4:
                    tone = "˥˩꜒꜔"
                else:
                    tone = MANDARIN_IPA_TONES[syllable_tone - 1]
            case _:
                tone = MANDARIN_IPA_TONES[syllable_tone - 1]

        res.append(normalize("NFC", glottal + initial + final + tone))

    return " ".join(res)


def segment_pinyin(
    pinyin: str,
    remove_special_characters: bool = True,
    remove_glob_characters: bool = True,
) -> tuple[bool, list[str]]:
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
        tuple[bool, list[str]]: Bool indicating whether Pinyin was valid, and
            list where each string is a valid Pinyin syllable, special
            character, or glob character
    """
    pinyin = pinyin.lower()
    valid_pinyin = True
    start_idx, end_idx, initial_found = 0, 0, False
    res = []

    while end_idx < len(pinyin):
        component_found = False

        curr_string = pinyin[end_idx]
        is_special_character = curr_string in SPECIAL_CHARACTERS
        is_glob_character = curr_string.strip() == "*" or curr_string.strip() == "?"

        if (
            curr_string == " "
            or curr_string == "'"
            or is_special_character
            or is_glob_character
        ):
            if initial_found:
                # Whitespace, apostrophes, special characters, and glob
                # characters mean that we *must* split a syllable
                syllable = pinyin[start_idx:end_idx]
                res.append(syllable)
                if syllable not in PINYIN_FINALS:
                    valid_pinyin = False
                start_idx = end_idx
                initial_found = False

            if not remove_glob_characters and is_glob_character:
                # Whitespace matters for glob characters! Consume
                # the next or previous whitespace if it exists and the
                # whitespace was not consumed by another syllable
                glob_start_idx = end_idx
                glob_end_idx = glob_start_idx + 1

                if (
                    (end_idx >= 1)
                    and (pinyin[end_idx - 1] == " ")
                    and (res and res[-1][-1] != " ")
                ):
                    # Keep whitespace preceding the glob character ONLY IF
                    # whitespace was not already added to the previous syllable
                    glob_start_idx -= 1
                if (len(pinyin) > (end_idx + 1)) and (pinyin[end_idx + 1] == " "):
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
            curr_string = pinyin[end_idx: end_idx + initial_len]
            if curr_string in PINYIN_INITIALS:
                if initial_found:
                    valid_pinyin = False
                end_idx += initial_len
                component_found = True
                initial_found = True
                break

        if component_found:
            continue

        for final_len in range(4, 0, -1):
            # Finals (nucleus + coda) can be length 4 or less; check for longer
            # finals before checking for shorter finals
            curr_string = pinyin[end_idx: end_idx + final_len]
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
    last_word = " ".join(last_word.split())
    last_word = last_word.strip()
    if last_word and last_word != "'":
        res.append(last_word)
        if last_word not in PINYIN_FINALS:
            valid_pinyin = False

    return [valid_pinyin, res]
