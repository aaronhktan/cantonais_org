def construct_romanization_query(syllables: list[str], delimiter: str) -> str:
    """Appends wildcard delimiter to each syllable if the syllable does
    not end with a digit.

    Args:
        syllables (list[str]): List of syllables
        delimiter (str): Character to append to each syllable

    Returns:
        str: All syllables in word list with appended wildcard delimiter
    """
    if not syllables:
        return ""

    processed_syllables = ""
    space_before_syllable = ""
    prev_syllable_added_delimiter = False
    for idx, syllable in enumerate(syllables):
        syllable = syllable.strip()
        if syllable[-1].isnumeric():
            processed_syllables += space_before_syllable + syllable
            space_before_syllable = " "
            prev_syllable_added_delimiter = False
        elif syllable == "*" or syllable == "?":
            if ((syllables[idx] == "*" or syllables[idx] == "?"
                    or syllables[idx] == "* " or syllables[idx] == "? ")
                    and prev_syllable_added_delimiter):
                # Replace delimiter in previous character with GLOB wildcard
                # if delimiter was attached to end of previous word
                processed_syllables = processed_syllables[:-len(delimiter)]
                processed_syllables += syllable
                space_before_syllable = ""
                prev_syllable_added_delimiter = False
        else:
            processed_syllables += space_before_syllable + syllable + delimiter
            space_before_syllable = " "
            prev_syllable_added_delimiter = True
    
    return processed_syllables
