import json

from . import chinese_utils
from ..models import (Definition, DefinitionsSet, Entry,
                      SourceSentence)


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


def prepare_jyutping_bind_values(jyutping: str) -> str:
    """Formats Jyutping bind value such that we respect exact matches, wildcards,
    and Jyutping segmentation

    Args:
        jyutping (str): String containing raw user input

    Returns:
        str: Formatted, segmented, cleaned up Jyutping string
    """
    # Exact match is specified by enclosing the query in double-quotes
    search_exact_match = (
        len(jyutping) >= 3 and jyutping[0] == "\"" and jyutping[-1] == "\"")
    # Wildcard character should only be appended if the last character is not "$"
    append_wildcard = not (jyutping[-1] == "$")

    if search_exact_match:
        # Remove the double-quotes
        jyutping_syllables = jyutping[1:-1].split()
    else:
        _, jyutping_syllables = chinese_utils.segment_jyutping(jyutping,
                                                               remove_glob_characters=False)

    if search_exact_match:
        query_param = " ".join(jyutping_syllables)
    else:
        query_param = construct_romanization_query(
            jyutping_syllables, "?")

    if append_wildcard and not search_exact_match:
        query_param += "*"

    return query_param


def prepare_pinyin_bind_values(pinyin: str) -> str:
    """Formats Pinyin bind value such that we respect exact matches, wildcards,
    and Pinyin segmentation

    Args:
        pinyin (str): String containing raw user input

    Returns:
        str: Formatted, segmented, cleaned up Pinyin string
    """
    # Exact match is specified by enclosing the query in double-quotes
    search_exact_match = (
        len(pinyin) >= 3 and pinyin[0] == "\"" and pinyin[-1] == "\"")
    # Wildcard character should only be appended if the last character is not "$"
    append_wildcard = not (pinyin[-1] == "$")

    if search_exact_match:
        # Remove the double-quotes
        pinyin_syllables = pinyin[1:-1].split()
    else:
        _, pinyin_syllables = chinese_utils.segment_pinyin(pinyin)

    if search_exact_match:
        query_param = " ".join(pinyin_syllables)
    else:
        query_param = construct_romanization_query(
            pinyin_syllables, "?")

    if append_wildcard and not search_exact_match:
        query_param += "*"

    return query_param


def parse_returned_records(records: list[str]) -> list[Entry]:
    """Parses records returned by a sequel query into a list of Entry objects.

    Args:
        records (list[str]): The result from a cursor.readall()

    Returns:
        list[Entry]: A list of entries parsed from the records provided by the cursor
    """
    res = []
    for record in records:
        sets = []
        definitions_col = json.loads(record[4])
        for definitions_group in definitions_col:
            definitions = []
            for definition in definitions_group["definitions"]:
                if not definition:
                    continue

                sentences = []
                if "sentences" in definition:
                    for sentence in definition["sentences"]:
                        if not sentence:
                            continue

                        translations = []
                        if sentence["translations"]:
                            for translation in sentence["translations"]:
                                translations.append(translation)
                        sentences.append(
                            SourceSentence(sentence["language"],
                                           sentence["simplified"],
                                           sentence["traditional"],
                                           sentence["jyutping"],
                                           sentence["pinyin"],
                                           translations=translations))

                definition_content = definition["definition"].replace(
                    r"\n", "\n")
                label = definition["label"] if "label" in definition else ""
                definitions.append(Definition(definition_content,
                                              label, sentences))
            sets.append(DefinitionsSet(definitions_group["source"],
                                       definitions))

        res.append(Entry(traditional=record[0], simplified=record[1],
                         jyutping=record[2], pinyin=record[3],
                         definitions_sets=sets))

    return res


def parse_existence(records: list[str]) -> bool:
    """Given a cursor's readall(), parses whether record contains 0 or 1

    Args:
        records (list[str]): Result from a cursor.readall()

    Returns:
        bool: True if the record contains 1, 0 otherwise
    """
    if len(records) > 1 or not len(records):
        return False

    record = records[0]
    existence_col = record[0]
    return existence_col
