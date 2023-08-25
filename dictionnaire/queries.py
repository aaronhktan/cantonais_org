import json
import os
import sqlite3

from flask import g

from .models import (Definition, DefinitionsSet, Entry,
                     SourceSentence, Translation, TranslationSet)
from .utils import chinese_utils, query_utils

DB_PATH = os.environ["CANTONAIS_ORG_DB_PATH"]


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)

    return g.db


def query_traditional(traditional):
    db = get_db()
    c = db.cursor()

    c.execute(
        """
WITH matching_entry_ids AS (
  SELECT rowid FROM entries WHERE traditional GLOB ?
  ),

matching_definition_ids AS (
  SELECT definition_id, definition FROM definitions WHERE fk_entry_id
  IN matching_entry_ids
  ),

matching_chinese_sentence_ids AS (
  SELECT definition_id, fk_chinese_sentence_id
  FROM matching_definition_ids AS mdi
  JOIN definitions_chinese_sentences_links AS dcsl ON
    mdi.definition_id = dcsl.fk_definition_id
    ),

matching_translations AS (
  SELECT mcsi.fk_chinese_sentence_id,
    json_group_array(DISTINCT
      json_object('sentence', sentence,
                  'language', language,
                  'direct', direct
    )) AS translation
  FROM matching_chinese_sentence_ids AS mcsi
  JOIN sentence_links AS sl ON mcsi.fk_chinese_sentence_id =
    sl.fk_chinese_sentence_id
  JOIN nonchinese_sentences AS ncs ON ncs.non_chinese_sentence_id =
    sl.fk_non_chinese_sentence_id
  GROUP BY mcsi.fk_chinese_sentence_id
  ),

matching_sentences AS (
 SELECT chinese_sentence_id, traditional, simplified, pinyin,
   jyutping, language
 FROM chinese_sentences AS cs
 WHERE chinese_sentence_id IN (
   SELECT fk_chinese_sentence_id FROM
     matching_chinese_sentence_ids
 )
 ),

matching_sentences_with_translations AS (
  SELECT chinese_sentence_id,
    json_object('traditional', traditional,
                'simplified', simplified,
                'pinyin', pinyin,
                'jyutping', jyutping,
                'language', language,
                'translations', json(translation)) AS sentence
  FROM matching_sentences AS ms
  LEFT JOIN matching_translations AS mt ON ms.chinese_sentence_id =
    mt.fk_chinese_sentence_id
    ),

matching_definitions AS (
  SELECT definition_id, fk_entry_id, fk_source_id, definition,
    label
  FROM definitions
  WHERE definitions.definition_id IN (
    SELECT definition_id FROM matching_definition_ids
  )
  ),

matching_definitions_with_sentences AS (
  SELECT fk_entry_id, fk_source_id,
    json_object('definition', definition,
                'label', label, 'sentences',
                json_group_array(json(sentence))) AS definition
  FROM matching_definitions AS md
  LEFT JOIN matching_chinese_sentence_ids AS mcsi ON
    md.definition_id = mcsi.definition_id
  LEFT JOIN matching_sentences_with_translations AS mswt ON
    mcsi.fk_chinese_sentence_id = mswt.chinese_sentence_id
  GROUP BY md.definition_id
  ),

matching_definition_groups AS (
  SELECT fk_entry_id,
    json_object('source', sourcename,
                'definitions',
                json_group_array(json(definition))) AS definitions
  FROM matching_definitions_with_sentences AS mdws
  LEFT JOIN sources ON sources.source_id = mdws.fk_source_id
  GROUP BY fk_entry_id, fk_source_id
  ),

matching_entries AS (
  SELECT simplified, traditional, jyutping, pinyin,
    json_group_array(json(definitions)) AS definitions
  FROM matching_definition_groups AS mdg
  LEFT JOIN entries ON entries.entry_id = mdg.fk_entry_id
  GROUP BY entry_id
  ORDER BY frequency DESC
  )

 SELECT traditional, simplified, jyutping, pinyin, definitions FROM
  matching_entries
""",
        (traditional,)
    )

    record = c.fetchone()

    entry = Entry(traditional=record[0], simplified=record[1],
                  jyutping=record[2], pinyin=record[3], definitions_sets=None)
    return entry


def get_traditional(traditional):
    db = get_db()
    c = db.cursor()

    c.execute(
        """
WITH matching_entry_ids AS (
  SELECT rowid FROM entries WHERE traditional GLOB ?
  ),

matching_definition_ids AS (
  SELECT definition_id, definition FROM definitions WHERE fk_entry_id
  IN matching_entry_ids
  ),

matching_chinese_sentence_ids AS (
  SELECT definition_id, fk_chinese_sentence_id
  FROM matching_definition_ids AS mdi
  JOIN definitions_chinese_sentences_links AS dcsl ON
    mdi.definition_id = dcsl.fk_definition_id
    ),

matching_translations AS (
  SELECT mcsi.fk_chinese_sentence_id,
    json_group_array(DISTINCT
      json_object('sentence', sentence,
                  'language', language,
                  'direct', direct
    )) AS translation
  FROM matching_chinese_sentence_ids AS mcsi
  JOIN sentence_links AS sl ON mcsi.fk_chinese_sentence_id =
    sl.fk_chinese_sentence_id
  JOIN nonchinese_sentences AS ncs ON ncs.non_chinese_sentence_id =
    sl.fk_non_chinese_sentence_id
  GROUP BY mcsi.fk_chinese_sentence_id
  ),

matching_sentences AS (
 SELECT chinese_sentence_id, traditional, simplified, pinyin,
   jyutping, language
 FROM chinese_sentences AS cs
 WHERE chinese_sentence_id IN (
   SELECT fk_chinese_sentence_id FROM
     matching_chinese_sentence_ids
 )
 ),

matching_sentences_with_translations AS (
  SELECT chinese_sentence_id,
    json_object('traditional', traditional,
                'simplified', simplified,
                'pinyin', pinyin,
                'jyutping', jyutping,
                'language', language,
                'translations', json(translation)) AS sentence
  FROM matching_sentences AS ms
  LEFT JOIN matching_translations AS mt ON ms.chinese_sentence_id =
    mt.fk_chinese_sentence_id
    ),

matching_definitions AS (
  SELECT definition_id, fk_entry_id, fk_source_id, definition,
    label
  FROM definitions
  WHERE definitions.definition_id IN (
    SELECT definition_id FROM matching_definition_ids
  )
  ),

matching_definitions_with_sentences AS (
  SELECT fk_entry_id, fk_source_id,
    json_object('definition', definition,
                'label', label, 'sentences',
                json_group_array(json(sentence))) AS definition
  FROM matching_definitions AS md
  LEFT JOIN matching_chinese_sentence_ids AS mcsi ON
    md.definition_id = mcsi.definition_id
  LEFT JOIN matching_sentences_with_translations AS mswt ON
    mcsi.fk_chinese_sentence_id = mswt.chinese_sentence_id
  GROUP BY md.definition_id
  ),

matching_definition_groups AS (
  SELECT fk_entry_id,
    json_object('source', sourcename,
                'definitions',
                json_group_array(json(definition))) AS definitions
  FROM matching_definitions_with_sentences AS mdws
  LEFT JOIN sources ON sources.source_id = mdws.fk_source_id
  GROUP BY fk_entry_id, fk_source_id
  ),

matching_entries AS (
  SELECT simplified, traditional, jyutping, pinyin,
    json_group_array(json(definitions)) AS definitions
  FROM matching_definition_groups AS mdg
  LEFT JOIN entries ON entries.entry_id = mdg.fk_entry_id
  GROUP BY entry_id
  ORDER BY frequency DESC
  )

 SELECT traditional, simplified, jyutping, pinyin, definitions FROM
  matching_entries
""",
        (traditional,)
    )

    record = c.fetchone()

    entry = Entry(traditional=record[0], simplified=record[1],
                  jyutping=record[2], pinyin=record[3], definitions_sets=None)
    return entry


def query_traditional(traditional):
    db = get_db()
    c = db.cursor()

    c.execute(
        """
WITH matching_entry_ids AS (
  SELECT rowid FROM entries WHERE traditional GLOB ?
  ),

matching_definition_ids AS (
  SELECT definition_id, definition FROM definitions WHERE fk_entry_id
  IN matching_entry_ids
  ),

matching_chinese_sentence_ids AS (
  SELECT definition_id, fk_chinese_sentence_id
  FROM matching_definition_ids AS mdi
  JOIN definitions_chinese_sentences_links AS dcsl ON
    mdi.definition_id = dcsl.fk_definition_id
    ),

matching_translations AS (
  SELECT mcsi.fk_chinese_sentence_id,
    json_group_array(DISTINCT
      json_object('sentence', sentence,
                  'language', language,
                  'direct', direct
    )) AS translation
  FROM matching_chinese_sentence_ids AS mcsi
  JOIN sentence_links AS sl ON mcsi.fk_chinese_sentence_id =
    sl.fk_chinese_sentence_id
  JOIN nonchinese_sentences AS ncs ON ncs.non_chinese_sentence_id =
    sl.fk_non_chinese_sentence_id
  GROUP BY mcsi.fk_chinese_sentence_id
  ),

matching_sentences AS (
 SELECT chinese_sentence_id, traditional, simplified, pinyin,
   jyutping, language
 FROM chinese_sentences AS cs
 WHERE chinese_sentence_id IN (
   SELECT fk_chinese_sentence_id FROM
     matching_chinese_sentence_ids
 )
 ),

matching_sentences_with_translations AS (
  SELECT chinese_sentence_id,
    json_object('traditional', traditional,
                'simplified', simplified,
                'pinyin', pinyin,
                'jyutping', jyutping,
                'language', language,
                'translations', json(translation)) AS sentence
  FROM matching_sentences AS ms
  LEFT JOIN matching_translations AS mt ON ms.chinese_sentence_id =
    mt.fk_chinese_sentence_id
    ),

matching_definitions AS (
  SELECT definition_id, fk_entry_id, fk_source_id, definition,
    label
  FROM definitions
  WHERE definitions.definition_id IN (
    SELECT definition_id FROM matching_definition_ids
  )
  ),

matching_definitions_with_sentences AS (
  SELECT fk_entry_id, fk_source_id,
    json_object('definition', definition,
                'label', label, 'sentences',
                json_group_array(json(sentence))) AS definition
  FROM matching_definitions AS md
  LEFT JOIN matching_chinese_sentence_ids AS mcsi ON
    md.definition_id = mcsi.definition_id
  LEFT JOIN matching_sentences_with_translations AS mswt ON
    mcsi.fk_chinese_sentence_id = mswt.chinese_sentence_id
  GROUP BY md.definition_id
  ),

matching_definition_groups AS (
  SELECT fk_entry_id,
    json_object('source', sourcename,
                'definitions',
                json_group_array(json(definition))) AS definitions
  FROM matching_definitions_with_sentences AS mdws
  LEFT JOIN sources ON sources.source_id = mdws.fk_source_id
  GROUP BY fk_entry_id, fk_source_id
  ),

matching_entries AS (
  SELECT simplified, traditional, jyutping, pinyin,
    json_group_array(json(definitions)) AS definitions
  FROM matching_definition_groups AS mdg
  LEFT JOIN entries ON entries.entry_id = mdg.fk_entry_id
  GROUP BY entry_id
  ORDER BY frequency DESC
  )

 SELECT traditional, simplified, jyutping, pinyin, definitions FROM
  matching_entries
""",
        (traditional,)
    )

    record = c.fetchone()

    entry = Entry(traditional=record[0], simplified=record[1],
                  jyutping=record[2], pinyin=record[3], definitions_sets=None)
    return entry


def query_simplified(simplified):
    db = get_db()
    c = db.cursor()

    c.execute(
        """
WITH matching_entry_ids AS (
  SELECT rowid FROM entries WHERE simplified GLOB ?
  ),

matching_definition_ids AS (
  SELECT definition_id, definition FROM definitions WHERE fk_entry_id
  IN matching_entry_ids
  ),

matching_chinese_sentence_ids AS (
  SELECT definition_id, fk_chinese_sentence_id
  FROM matching_definition_ids AS mdi
  JOIN definitions_chinese_sentences_links AS dcsl ON
    mdi.definition_id = dcsl.fk_definition_id
    ),

matching_translations AS (
  SELECT mcsi.fk_chinese_sentence_id,
    json_group_array(DISTINCT
      json_object('sentence', sentence,
                  'language', language,
                  'direct', direct
    )) AS translation
  FROM matching_chinese_sentence_ids AS mcsi
  JOIN sentence_links AS sl ON mcsi.fk_chinese_sentence_id =
    sl.fk_chinese_sentence_id
  JOIN nonchinese_sentences AS ncs ON ncs.non_chinese_sentence_id =
    sl.fk_non_chinese_sentence_id
  GROUP BY mcsi.fk_chinese_sentence_id
  ),

matching_sentences AS (
 SELECT chinese_sentence_id, traditional, simplified, pinyin,
   jyutping, language
 FROM chinese_sentences AS cs
 WHERE chinese_sentence_id IN (
   SELECT fk_chinese_sentence_id FROM
     matching_chinese_sentence_ids
 )
 ),

matching_sentences_with_translations AS (
  SELECT chinese_sentence_id,
    json_object('traditional', traditional,
                'simplified', simplified,
                'pinyin', pinyin,
                'jyutping', jyutping,
                'language', language,
                'translations', json(translation)) AS sentence
  FROM matching_sentences AS ms
  LEFT JOIN matching_translations AS mt ON ms.chinese_sentence_id =
    mt.fk_chinese_sentence_id
    ),

matching_definitions AS (
  SELECT definition_id, fk_entry_id, fk_source_id, definition,
    label
  FROM definitions
  WHERE definitions.definition_id IN (
    SELECT definition_id FROM matching_definition_ids
  )
  ),

matching_definitions_with_sentences AS (
  SELECT fk_entry_id, fk_source_id,
    json_object('definition', definition,
                'label', label, 'sentences',
                json_group_array(json(sentence))) AS definition
  FROM matching_definitions AS md
  LEFT JOIN matching_chinese_sentence_ids AS mcsi ON
    md.definition_id = mcsi.definition_id
  LEFT JOIN matching_sentences_with_translations AS mswt ON
    mcsi.fk_chinese_sentence_id = mswt.chinese_sentence_id
  GROUP BY md.definition_id
  ),

matching_definition_groups AS (
  SELECT fk_entry_id,
    json_object('source', sourcename,
                'definitions',
                json_group_array(json(definition))) AS definitions
  FROM matching_definitions_with_sentences AS mdws
  LEFT JOIN sources ON sources.source_id = mdws.fk_source_id
  GROUP BY fk_entry_id, fk_source_id
  ),

matching_entries AS (
  SELECT simplified, traditional, jyutping, pinyin,
    json_group_array(json(definitions)) AS definitions
  FROM matching_definition_groups AS mdg
  LEFT JOIN entries ON entries.entry_id = mdg.fk_entry_id
  GROUP BY entry_id
  ORDER BY frequency DESC
  )

 SELECT traditional, simplified, jyutping, pinyin, definitions FROM
  matching_entries
""",
        (simplified,)
    )

    record = c.fetchone()

    entry = Entry(traditional=record[0], simplified=record[1],
                  jyutping=record[2], pinyin=record[3], definitions_sets=None)
    return entry


def query_jyutping(jyutping: str) -> Entry | None:
    db = get_db()
    c = db.cursor()

    # Exact match is specified by enclosing the query in double-quotes
    search_exact_match = (
        len(jyutping) >= 3 and jyutping[0] == "\"" and jyutping[-1] == "\"")
    # Wildcard character should only be appended if the last character is not "$"
    append_wildcard = not (jyutping[-1] == "$")

    if search_exact_match:
        # Remove the double-quotes
        jyutping_syllables = jyutping[1:-1].split()
    else:
        jyutping_syllables = chinese_utils.segment_jyutping(jyutping)

    if search_exact_match:
        query_param = " ".join(jyutping_syllables)
    else:
        query_param = query_utils.construct_romanization_query(
            jyutping_syllables, "?")

    if append_wildcard and not search_exact_match:
        query_param += "*"

    c.execute(
        """
WITH matching_entry_ids AS (
  SELECT rowid FROM entries WHERE jyutping GLOB ?
  ),

matching_definition_ids AS (
  SELECT definition_id, definition FROM definitions WHERE fk_entry_id
  IN matching_entry_ids
  ),

matching_chinese_sentence_ids AS (
  SELECT definition_id, fk_chinese_sentence_id
  FROM matching_definition_ids AS mdi
  JOIN definitions_chinese_sentences_links AS dcsl ON
    mdi.definition_id = dcsl.fk_definition_id
    ),

matching_translations AS (
  SELECT mcsi.fk_chinese_sentence_id,
    json_group_array(DISTINCT
      json_object('sentence', sentence,
                  'language', language,
                  'direct', direct
    )) AS translation
  FROM matching_chinese_sentence_ids AS mcsi
  JOIN sentence_links AS sl ON mcsi.fk_chinese_sentence_id =
    sl.fk_chinese_sentence_id
  JOIN nonchinese_sentences AS ncs ON ncs.non_chinese_sentence_id =
    sl.fk_non_chinese_sentence_id
  GROUP BY mcsi.fk_chinese_sentence_id
  ),

matching_sentences AS (
 SELECT chinese_sentence_id, traditional, simplified, pinyin,
   jyutping, language
 FROM chinese_sentences AS cs
 WHERE chinese_sentence_id IN (
   SELECT fk_chinese_sentence_id FROM
     matching_chinese_sentence_ids
 )
 ),

matching_sentences_with_translations AS (
  SELECT chinese_sentence_id,
    json_object('traditional', traditional,
                'simplified', simplified,
                'pinyin', pinyin,
                'jyutping', jyutping,
                'language', language,
                'translations', json(translation)) AS sentence
  FROM matching_sentences AS ms
  LEFT JOIN matching_translations AS mt ON ms.chinese_sentence_id =
    mt.fk_chinese_sentence_id
    ),

matching_definitions AS (
  SELECT definition_id, fk_entry_id, fk_source_id, definition,
    label
  FROM definitions
  WHERE definitions.definition_id IN (
    SELECT definition_id FROM matching_definition_ids
  )
  ),

matching_definitions_with_sentences AS (
  SELECT fk_entry_id, fk_source_id,
    json_object('definition', definition,
                'label', label, 'sentences',
                json_group_array(json(sentence))) AS definition
  FROM matching_definitions AS md
  LEFT JOIN matching_chinese_sentence_ids AS mcsi ON
    md.definition_id = mcsi.definition_id
  LEFT JOIN matching_sentences_with_translations AS mswt ON
    mcsi.fk_chinese_sentence_id = mswt.chinese_sentence_id
  GROUP BY md.definition_id
  ),

matching_definition_groups AS (
  SELECT fk_entry_id,
    json_object('source', sourcename,
                'definitions',
                json_group_array(json(definition))) AS definitions
  FROM matching_definitions_with_sentences AS mdws
  LEFT JOIN sources ON sources.source_id = mdws.fk_source_id
  GROUP BY fk_entry_id, fk_source_id
  ),

matching_entries AS (
  SELECT simplified, traditional, jyutping, pinyin,
    json_group_array(json(definitions)) AS definitions
  FROM matching_definition_groups AS mdg
  LEFT JOIN entries ON entries.entry_id = mdg.fk_entry_id
  GROUP BY entry_id
  ORDER BY frequency DESC
  )

 SELECT traditional, simplified, jyutping, pinyin, definitions FROM
  matching_entries
""",
        (query_param,)
    )

    records = c.fetchall()
    if not records:
        return None

    for record in records:
        sets = []
        definitions_col = json.loads(record[4])
        for definitions_group in definitions_col:
            definitions = []
            for definition in definitions_group["definitions"]:
                sentences = []
                for sentence in definition["sentences"]:
                    translations = []
                    for translation in sentence["translations"]:
                        translations.append(translation)
                    sentences.append(SourceSentence(sentence["language"],
                                                    sentence["simplified"],
                                                    sentence["traditional"],
                                                    sentence["jyutping"],
                                                    sentence["pinyin"],
                                                    translations=translations))
                definition_content = definition["definition"].replace(r"\n","\n")
                print(definition_content)
                definitions.append(Definition(definition_content,
                                              definition["label"], sentences))
            sets.append(DefinitionsSet(definitions_group["source"],
                                       definitions))

        entry = Entry(traditional=record[0], simplified=record[1],
                      jyutping=record[2], pinyin=record[3],
                      definitions_sets=sets)
        return entry


def query_pinyin(pinyin: str) -> Entry | None:
    db = get_db()
    c = db.cursor()

    c.execute(
        """
WITH matching_entry_ids AS (
  SELECT rowid FROM entries WHERE pinyin GLOB ?
  ),

matching_definition_ids AS (
  SELECT definition_id, definition FROM definitions WHERE fk_entry_id
  IN matching_entry_ids
  ),

matching_chinese_sentence_ids AS (
  SELECT definition_id, fk_chinese_sentence_id
  FROM matching_definition_ids AS mdi
  JOIN definitions_chinese_sentences_links AS dcsl ON
    mdi.definition_id = dcsl.fk_definition_id
    ),

matching_translations AS (
  SELECT mcsi.fk_chinese_sentence_id,
    json_group_array(DISTINCT
      json_object('sentence', sentence,
                  'language', language,
                  'direct', direct
    )) AS translation
  FROM matching_chinese_sentence_ids AS mcsi
  JOIN sentence_links AS sl ON mcsi.fk_chinese_sentence_id =
    sl.fk_chinese_sentence_id
  JOIN nonchinese_sentences AS ncs ON ncs.non_chinese_sentence_id =
    sl.fk_non_chinese_sentence_id
  GROUP BY mcsi.fk_chinese_sentence_id
  ),

matching_sentences AS (
 SELECT chinese_sentence_id, traditional, simplified, pinyin,
   jyutping, language
 FROM chinese_sentences AS cs
 WHERE chinese_sentence_id IN (
   SELECT fk_chinese_sentence_id FROM
     matching_chinese_sentence_ids
 )
 ),

matching_sentences_with_translations AS (
  SELECT chinese_sentence_id,
    json_object('traditional', traditional,
                'simplified', simplified,
                'pinyin', pinyin,
                'jyutping', jyutping,
                'language', language,
                'translations', json(translation)) AS sentence
  FROM matching_sentences AS ms
  LEFT JOIN matching_translations AS mt ON ms.chinese_sentence_id =
    mt.fk_chinese_sentence_id
    ),

matching_definitions AS (
  SELECT definition_id, fk_entry_id, fk_source_id, definition,
    label
  FROM definitions
  WHERE definitions.definition_id IN (
    SELECT definition_id FROM matching_definition_ids
  )
  ),

matching_definitions_with_sentences AS (
  SELECT fk_entry_id, fk_source_id,
    json_object('definition', definition,
                'label', label, 'sentences',
                json_group_array(json(sentence))) AS definition
  FROM matching_definitions AS md
  LEFT JOIN matching_chinese_sentence_ids AS mcsi ON
    md.definition_id = mcsi.definition_id
  LEFT JOIN matching_sentences_with_translations AS mswt ON
    mcsi.fk_chinese_sentence_id = mswt.chinese_sentence_id
  GROUP BY md.definition_id
  ),

matching_definition_groups AS (
  SELECT fk_entry_id,
    json_object('source', sourcename,
                'definitions',
                json_group_array(json(definition))) AS definitions
  FROM matching_definitions_with_sentences AS mdws
  LEFT JOIN sources ON sources.source_id = mdws.fk_source_id
  GROUP BY fk_entry_id, fk_source_id
  ),

matching_entries AS (
  SELECT simplified, traditional, jyutping, pinyin,
    json_group_array(json(definitions)) AS definitions
  FROM matching_definition_groups AS mdg
  LEFT JOIN entries ON entries.entry_id = mdg.fk_entry_id
  GROUP BY entry_id
  ORDER BY frequency DESC
  )

 SELECT traditional, simplified, jyutping, pinyin, definitions FROM
  matching_entries
""",
        (pinyin,)
    )

    record = c.fetchall()
    if not record:
        return None

    entry = Entry(traditional=record[0], simplified=record[1],
                  jyutping=record[2], pinyin=record[3], definitions_sets=None)
    return entry
