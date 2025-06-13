import re

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

JYUTPING_INITIALS = (
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
    "ng",
    "h",
    "gw",
    "kw",
    "w",
    "z",
    "c",
    "s",
    "j",
    "m",
)

JYUTPING_FINALS = (
    "a",
    "aa",
    "aai",
    "aau",
    "aam",
    "aan",
    "aang",
    "aap",
    "aat",
    "aak",
    "ai",
    "au",
    "am",
    "an",
    "ang",
    "ap",
    "at",
    "ak",
    "e",
    "ei",
    "eu",
    "em",
    "en",
    "eng",
    "ep",
    "ek",
    "i",
    "iu",
    "im",
    "in",
    "ing",
    "ip",
    "it",
    "ik",
    "o",
    "oi",
    "ou",
    "on",
    "ong",
    "ot",
    "ok",
    "u",
    "ui",
    "un",
    "ung",
    "ut",
    "uk",
    "oe",
    "oet",
    "eoi",
    "eon",
    "oeng",
    "eot",
    "oek",
    "yu",
    "yun",
    "yut",
    "m",
    "ng",
)

JYUTPING_TONES = (1, 2, 3, 4, 5, 6)

YALE_INITIAL_REGEX = (
    (re.compile(r"^jy?"), "y"),
    (re.compile(r"^z"), "j"),
    (re.compile(r"^c"), "ch"),
)

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

CANTONESE_IPA_REGEX = re.compile(
    r"([bcdfghjklmnpqrstvwxyz]?"
    r"[bcdfghjklmnpqrstvwxyz]"
    r"?)([a@e>i|o~u^y][eo]?)"
    r"([iuymngptk]?g?)([1-9])"
)
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


def jyutping_to_yale(jyutping: str, use_spaces_to_segment: bool = False) -> str:
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
                final = (
                    f"{final[:vowel_idx]}"
                    f"{YALE_VOWEL_REPLACEMENTS[vowel][tone - 1]}"
                    f"{final[vowel_idx + 1:]}"
                )
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
        _, syllables = segment_jyutping(
            jyutping, remove_special_characters=False, remove_glob_characters=False
        )

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
        _, syllables = segment_jyutping(
            jyutping, remove_special_characters=False, remove_glob_characters=False
        )

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
                CANTONESE_IPA_TONES[tone - 1], syllable
            )

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


def jyutping_autocorrect(
        jyutping: str
) -> str:
    """Attempts to correct for common misspellings for Jyutping syllables.

    Args:
        jyutping (str): Raw Jyutping or Jyutping-adjacent string to correct

    Returns:
        str: Corrected Jyutping string, formatted with REGEX operators "()",
        "|", "?" (notated as "!") in case of ambiguity.
    """
    result = jyutping

    # This is for some romanizations like "shui" for 水
    # And needs to happen before the "sh" -> "s" conversion
    result = result.replace("hui", "heoi")

    # The initial + nucleus "cu-" never appears in Jyutping, so the user
    # probably intended to make the IPA [kʰɐ] sound
    # Surround the k with capturing group to prevent replacement with (g|k)
    # if sound changes are enabled
    result = result.replace("cu", "(k)u")

    # "x" never appears in Jyutping, the user might be more familiar
    # with Pinyin and assume that it's an "s" sound
    result = result.replace("x", "s")

    result = result.replace("ch", "c")
    result = result.replace("sh", "s")
    result = result.replace("zh", "z")

    result = result.replace("eung", "oeng")
    result = result.replace("erng", "oeng")

    result = result.replace("eui", "eoi")
    result = result.replace("euk", "oek")
    result = result.replace("eun", "(eo|yu)n")
    result = result.replace("eut", "(eo|yu)t")
    result = result.replace("eu", "(e|y)u")
    result = result.replace("ern", "eon")

    idx = result.find("oen")
    while idx != -1:
        if result[idx:idx+4] == "oeng":
            pass
        else:
            result = result[:idx] + "eon" + result[idx+3:]
        idx = result.find("oen", idx+1)

    result = result.replace("oei", "eoi")
    result = result.replace("oet", "eot")

    result = result.replace("eong ", "oeng ")
    result = result.replace("eong'", "oeng'")
    if result.endswith("eong"):
        idx = result.rfind("eong")
        result = result[:idx] + "oeng"
    result = result.replace("eok", "oek")

    result = result.replace("ar", "aa")
    result = result.replace("ee", "i")
    result = result.replace("ay", "ei")
    result = result.replace("oy", "oi")
    result = result.replace("oo", "(y!u)")
    result = result.replace("ong", "(o|u)ng")
    result = result.replace("young", "jung")

    result = result.replace("yue", "jyu")
    result = result.replace("ue", "(yu)")
    result = result.replace("tsz", "zi")
    result = result.replace("ck", "k")

    result = result.replace("ck", "k")

    # The following changes may be unsafe because it is ambiguous whether
    # they are final + initial or a "misspelling" of a final
    # However, it is unambiguous if there is a separator at the end of the
    # syllable, or it is the end of the string

    # 2. Check if the user intends to write an [-ɛː j-] or [-ei̯] cluster
    result = result.replace("ey ", "ei ")
    result = result.replace("ey'", "ei'")
    if result.endswith("ey"):
        result = result[:len(result)-2] + "ei"

    # Initials for which <initial> + "-ei" exist in Jyutping
    close_front_cluster = ("p", "f", "d", "n", "l", "h", "w")
    # Initials for which <initial> + "-e j-" exist in Jyutping
    open_mid_cluster = ("c", "j", "y")
    # Initials for which both exist in Jyutping
    ambiguous_cluster = ("b", "m", "g", "k", "z", "s")

    idx = result.find("ey")
    while idx != -1:
        match idx:
            case 0:
                result = "ei" + result[2:]
            case _:
                initial_idx = idx - 1
                if idx >= 2 and result[initial_idx] == ")":
                    initial_idx = idx - 2

                if result[initial_idx] in close_front_cluster:
                    result = result[:idx] + "ei" + result[idx+2:]
                elif result[initial_idx] in open_mid_cluster:
                    result = result[:idx] + "e j" + result[idx+2:]
                elif result[initial_idx] in ambiguous_cluster:
                    # The [j-] cluster can only occur if what follows is not an initial
                    initial_found = False
                    for initial_len in range(2, 0, -1):
                        initial = result[idx+2:idx+2+initial_len]
                        if initial in JYUTPING_INITIALS or initial == "y":
                            initial_found = True
                    if initial_found:
                        result = result[:idx] + "ei" + result[idx+2:]
                    else:
                        result = result[:idx] + "e j" + result[idx+2:]
        idx = result.find("ey", idx+1)

    # 3. Check if the user intends to write an [-ɔː h-] or [-ou̯] cluster
    result = result.replace("oh ", "ou ")
    result = result.replace("oh'", "ou'")
    if result.endswith("oh"):
        result = result[:len(result)-2] + "ou"

    # Initials for which <initial> + "-ou" exist in Jyutping
    close_back_cluster = ("n", "j")
    # Initials for which both "-ou" and "-o h-" exist in Jyutping
    ambiguous_cluster = ("b", "p", "m", "f", "d", "t", "l", "g", "h", "w", "z", "c", "s")

    idx = result.find("oh")
    while idx != -1:
        match idx:
            case 0:
                result = "ou" + result[2:]
            case _:
                initial_idx = idx - 1
                if idx >= 2 and result[initial_idx] == ")":
                    initial_idx = idx - 2

                if result[initial_idx] in close_back_cluster:
                    result = result[:idx] + "ou" + result[idx+2:]
                elif result[initial_idx] in ambiguous_cluster:
                    # The [h-] cluster can only occur if what follows is not an initial
                    initial_found = False
                    for initial_len in range(2, 0, -1):
                        initial = result[idx+2:idx+2+initial_len]
                        if initial in JYUTPING_INITIALS or initial == "y":
                            initial_found = True
                    if initial_found:
                        result = result[:idx] + "ou" + result[idx+2:]
                    else:
                        result = result[:idx] + "e h" + result[idx+2:]
        idx = result.find("oh", idx+1)

    # 4. Check if the user intends to write an [-ɔː w-] or [-auː] cluster
    result = result.replace("ow ", "au ")
    result = result.replace("ow'", "au'")
    if result.endswith("ow"):
        result = result[:len(result)-2] + "au"

    # Initials for which <initial> + "-(a)au" exist in Jyutping
    close_back_cluster = ("b", "m", "k", "s")
    # Initials for which both "-o w-" and "-(a)au" exist in Jyutping
    ambiguous_cluster = ("p", "m", "f", "d", "t", "n", "l", "g", "h", "z", "c", "s")

    idx = result.find("ow")
    while idx != -1:
        match idx:
            case 0:
                result = "au" + result[2:]
            case _:
                initial_idx = idx - 1
                if idx >= 2 and result[initial_idx] == ")":
                    initial_idx = idx - 2

                if result[initial_idx] in close_back_cluster:
                    result = result[:idx] + "au" + result[idx+2:]
                elif result[initial_idx] in ambiguous_cluster:
                    # The [h-] cluster can only occur if what follows is not an initial
                    initial_found = False
                    for initial_len in range(2, 0, -1):
                        initial = result[idx+2:idx+2+initial_len]
                        if initial in JYUTPING_INITIALS or initial == "y":
                            initial_found = True
                    if initial_found:
                        result = result[:idx] + "au" + result[idx+2:]
                    else:
                        result = result[:idx] + "o w" + result[idx+2:]
        idx = result.find("oh", idx+1)

    # 5. Check if the user intends to write an [ɐm] or [-uː  m-] cluster
    result = result.replace("um ", "am ")
    result = result.replace("um'", "am'")
    if result.endswith("um"):
        result = result[:len(result)-2] + "am"

    # Initials for which <initial> + "-am" exist in Jyutping
    open_mid_central_cluster = ("b", "p", "m", "d", "t", "n", "l", "k", "h", "z", "c", "s")
    # Initials for which both "-o w-" and "-(a)au" exist in Jyutping
    close_back_cluster = ("f", "w", "a", "e", "i", "o")

    idx = result.find("um")
    while idx != -1:
        match idx:
            case 0:
                result = "am" + result[2:]
            case _:
                initial_idx = idx - 1
                if idx >= 2 and result[initial_idx] == ")":
                    initial_idx = idx - 2

                if result[initial_idx] in open_mid_central_cluster:
                    result = result[:idx] + "am" + result[idx+2:]
                elif result[initial_idx] in close_back_cluster:
                    pass
                elif result[initial_idx] == "g":
                    # The [m-] cluster can only occur if what follows is not an initial
                    initial_found = False
                    for initial_len in range(2, 0, -1):
                        initial = result[idx+2:idx+2+initial_len]
                        if initial in JYUTPING_INITIALS or initial == "y":
                            initial_found = True
                    if initial_found:
                        result = result[:idx] + "am" + result[idx+2:]
                    else:
                        result = result[:idx] + "u m" + result[idx+2:]
        idx = result.find("um", idx+1)

    # 6. Check if the user intends to write an [-yː j-] or [-ɐm] cluster
    # Initials for which <initial> + "-yu m-" exist in Jyutping
    close_front_cluster = ("z", "c", "s", "j")

    idx = result.find("yum")
    while idx != -1:
        match idx:
            case 0:
                result = "jam" + result[3:]
            case _:
                initial_idx = idx - 1
                if idx >= 2 and result[initial_idx] == ")":
                    initial_idx = idx - 2

                if result[initial_idx] in close_front_cluster:
                    result = result[:idx] + "yu m" + result[idx+3:]
                else:
                    result = result[:idx] + "jam" + result[idx+3:]
        idx = result.find("yum", idx+1)

    # 7. Check if the user intends to write an [-yː p-] or [-ɐp] cluster
    # Initials for which <initial> + "-yu p-" exist in Jyutping
    close_front_cluster = ("z", "s", "j")

    idx = result.find("yup")
    while idx != -1:
        match idx:
            case 0:
                result = "jap" + result[3:]
            case _:
                initial_idx = idx - 1
                if idx >= 2 and result[initial_idx] == ")":
                    initial_idx = idx - 2

                if result[initial_idx] in close_front_cluster:
                    result = result[:idx] + "yu p" + result[idx+3:]
                else:
                    result = result[:idx] + "jap" + result[idx+3:]
        idx = result.find("yup", idx+1)

    # 8. Check if the user intends to write an [-yː k-] or [jʊk] cluster
    # Initials for which <initial> + "-yu k-" exist in Jyutping
    close_front_cluster = ("z", "s", "c", "j")

    idx = result.find("yuk")
    while idx != -1:
        match idx:
            case 0:
                result = "juk" + result[3:]
            case _:
                initial_idx = idx - 1
                if idx >= 2 and result[initial_idx] == ")":
                    initial_idx = idx - 2

                if result[initial_idx] in close_front_cluster:
                    result = result[:idx] + "yu k" + result[idx+3:]
                else:
                    result = result[:idx] + "juk" + result[idx+3:]
        idx = result.find("yuk", idx+1)

    # 9. Check if the user intends to write an [-yn g-] or [jʊŋ] cluster
    # Initials for which <initial> + "-yun g-" exist in Jyutping
    close_front_cluster = ("z", "s", "c", "j")

    idx = result.find("yung")
    while idx != -1:
        match idx:
            case 0:
                result = "jung" + result[4:]
            case _:
                initial_idx = idx - 1
                if idx >= 2 and result[initial_idx] == ")":
                    initial_idx = idx - 2

                if result[initial_idx] in close_front_cluster:
                    result = result[:idx] + "(yu)n g" + result[idx+4:]
                else:
                    result = result[:idx] + "jung" + result[idx+4:]
        idx = result.find("yung", idx+1)

    # 10. Check if the user intends to write an [-yn] or [jɐn], [jyn], [yn] cluster
    # Initials for which <initial> + "-yu n-" exist in Jyutping
    close_front_cluster = ("z", "s", "c", "j")

    idx = result.find("yun")
    while idx != -1:
        match idx:
            case 0:
                result = "j(a|yu)n" + result[3:]
            case _:
                initial_idx = idx - 1
                if idx >= 2 and result[initial_idx] == ")":
                    initial_idx = idx - 2

                if result[initial_idx] in close_front_cluster:
                    result = result[:idx] + "yun" + result[idx+3:]
                else:
                    result = result[:idx] + "j(a|yu)n" + result[idx+3:]
        idx = result.find("yun", idx+1)

    # 11. Check if the user intends to write an [-yt] or [jɐt], [jyt], [yt] cluster
    # Initials for which <initial> + "-yu t-" exist in Jyutping
    close_front_cluster = ("z", "s", "c", "j")

    idx = result.find("yut")
    while idx != -1:
        match idx:
            case 0:
                result = "j(a|yu)t" + result[3:]
            case _:
                initial_idx = idx - 1
                if idx >= 2 and result[initial_idx] == ")":
                    initial_idx = idx - 2

                if result[initial_idx] in close_front_cluster:
                    result = result[:idx] + "(yu)t" + result[idx+3:]
                else:
                    result = result[:idx] + "(ja|jyu|yu)t" + result[idx+3:]
        idx = result.find("yut", idx+1)

    # Unsafe because it is ambiguous whether these are final + initial
    # or a "misspelling" of an initial
    # But unambiguous if they are at the start of a syllable
    if result.startswith("ts"):
        result = "c" + result[2:]
    result = result.replace(" ts", "c")
    if result.startswith("kwu"):
        result = "(g|k)w!u" + result[3:]
    result = result.replace("kwu", "(g|k)w!u")

    # Change any "y" that is not followed by a "u" to "j"
    # This needs to happen before the final replacements
    idx = result.find("y")
    while idx != -1:
        if result[idx:idx+2] == "yu" or result[idx:idx+3] in ("y!u", "y)u"):
            pass
        else:
            result = result[:idx] + "j" + result[idx+1:]
        idx = result.find("y", idx+1)

    result = result.replace("ui", "(eo|u)i")
    result = result.replace("un", "(y!u|a|eo)n")
    result = result.replace("ut", "(a|u)t")

    return result


def segment_jyutping(
    jyutping: str,
    remove_special_characters: bool = True,
    remove_glob_characters: bool = True,
) -> tuple[bool, list[str]]:
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
        tuple[bool, list[str]]: Bool indicating whether Jyutping was valid,
            and list where each string is a valid Jyutping syllable,
            special character, or glob character
    """
    jyutping = jyutping.lower()
    valid_jyutping = True
    start_idx, end_idx, initial_found = 0, 0, False
    res = []

    while end_idx < len(jyutping):
        component_found = False

        curr_string = jyutping[end_idx]
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
                syllable = jyutping[start_idx:end_idx]
                res.append(syllable)
                if syllable not in JYUTPING_FINALS:
                    valid_jyutping = True
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
                    and (jyutping[end_idx - 1] == " ")
                    and (res and res[-1][-1] != " ")
                ):
                    # Keep whitespace preceding the glob character ONLY IF
                    # whitespace was not already added to the previous syllable
                    glob_start_idx -= 1
                if (len(jyutping) > (end_idx + 1)) and (jyutping[end_idx + 1] == " "):
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
            curr_string = jyutping[end_idx: end_idx + initial_len]

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
                else:
                    valid_jyutping = False

            end_idx += initial_len
            initial_found = True
            component_found = True

        if component_found:
            continue

        for final_len in range(4, 0, -1):
            # Finals (nucleus + coda) can be length 4 or less; check for longer
            # finals before checking for shorter finals
            curr_string = jyutping[end_idx: end_idx + final_len]
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
        else:
            valid_jyutping = False

        end_idx += 1

    # Add whatever's left in the search term, minus whitespace
    last_word = jyutping[start_idx:]
    last_word = " ".join(last_word.split())
    last_word = last_word.strip()
    if last_word and last_word != "'":
        res.append(last_word)
        if last_word not in JYUTPING_FINALS:
            valid_jyutping = False

    return [valid_jyutping, res]
