import json

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


def parse_returned_records(records: list[str]) -> list[Entry]:
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
