import os
import re
import sqlite3

from collections import defaultdict

from flask import g

from .models import Entry, SourceSentence
from .utils import chinese_utils, query_utils

DB_PATH = os.environ["CANTONAIS_ORG_DB_PATH"]
REGEX_OPERATOR = "REGEXP"
GLOB_OPERATOR = "GLOB"

print(f"database path: {DB_PATH}")

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)

    def regexp(y, x, search=re.search):
        return 1 if search(y, x) else 0

    g.db.create_function("REGEXP", 2, regexp)

    return g.db


def get_traditional(traditional: str) -> list[Entry] | None:
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
        (traditional,),
    )

    records = c.fetchall()
    if not records:
        return None

    return query_utils.parse_returned_records(records)


def get_example_sample(param: str) -> dict[str, SourceSentence] | None:
    examples = query_examples(param)

    # Display only a subset of the examples on the entry page
    example_sample = defaultdict(list)

    if not examples:
        return None

    for example in examples:
        for translations_set in example.translations:
            source = translations_set.source

            if len(example_sample[source]) >= 5:
                continue

            sample = SourceSentence(
                example.source_language,
                example.simplified,
                example.traditional,
                example.jyutping,
                example.pinyin,
                translations=translations_set,
            )
            example_sample[source].append(sample)

    return dict(example_sample)


def query_traditional(traditional: str) -> list[Entry] | None:
    db = get_db()
    c = db.cursor()

    # Exact match is specified by enclosing the query in double-quotes
    search_exact_match = (
        len(traditional) >= 3 and traditional[0] == '"' and traditional[-1] == '"'
    )
    # Wildcard character should only be appended if the last character is not "$"
    append_wildcard = not (traditional[-1] == "$")

    if search_exact_match:
        # Remove double-quotes
        query_param = traditional[1:-1]
    elif not append_wildcard:
        # Remove the end position marker
        query_param = traditional[:-1]
    else:
        query_param = f"{traditional}*"

    c.execute(
        """
WITH matching_entry_ids AS (
  SELECT rowid FROM entries WHERE traditional GLOB ?
),

matching_definition_ids AS (
  SELECT definition_id, definition FROM definitions WHERE fk_entry_id
    IN matching_entry_ids
),

matching_definitions AS (
  SELECT definition_id, fk_entry_id, fk_source_id, definition,
    label
  FROM definitions
  WHERE definitions.definition_id IN (
    SELECT definition_id FROM matching_definition_ids
  )
),

matching_definition_groups AS (
  SELECT fk_entry_id,
    json_object('source', sourcename,
                'definitions',
                json_group_array(json_object(
                  'definition', definition))) AS definitions
  FROM matching_definitions AS md
  LEFT JOIN sources ON sources.source_id = md.fk_source_id
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
        (query_param,),
    )

    records = c.fetchall()
    if not records:
        return None

    return query_utils.parse_returned_records(records)


def query_simplified(simplified: str) -> list[Entry] | None:
    db = get_db()
    c = db.cursor()

    # Exact match is specified by enclosing the query in double-quotes
    search_exact_match = (
        len(simplified) >= 3 and simplified[0] == '"' and simplified[-1] == '"'
    )
    # Wildcard character should only be appended if the last character is not "$"
    append_wildcard = not (simplified[-1] == "$")

    if search_exact_match:
        # Remove double-quotes
        query_param = simplified[1:-1]
    elif not append_wildcard:
        # Remove the end position marker
        query_param = simplified[:-1]
    else:
        query_param = f"{simplified}*"

    c.execute(
        """
WITH matching_entry_ids AS (
  SELECT rowid FROM entries WHERE simplified GLOB ?
),

matching_definition_ids AS (
  SELECT definition_id, definition FROM definitions WHERE fk_entry_id
    IN matching_entry_ids
),

matching_definitions AS (
  SELECT definition_id, fk_entry_id, fk_source_id, definition,
    label
  FROM definitions
  WHERE definitions.definition_id IN (
    SELECT definition_id FROM matching_definition_ids
  )
),

matching_definition_groups AS (
  SELECT fk_entry_id,
    json_object('source', sourcename,
                'definitions',
                json_group_array(json_object(
                  'definition', definition))) AS definitions
  FROM matching_definitions AS md
  LEFT JOIN sources ON sources.source_id = md.fk_source_id
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
        (query_param,),
    )

    records = c.fetchall()
    if not records:
        return None

    return query_utils.parse_returned_records(records)


def query_jyutping(jyutping: str, fuzzy: bool) -> Entry | None:
    db = get_db()
    c = db.cursor()

    query_param = query_utils.prepare_jyutping_bind_values(jyutping, fuzzy)

    if fuzzy:
        operator = REGEX_OPERATOR
    else:
        operator = GLOB_OPERATOR

    c.execute(
        f"""
WITH matching_entry_ids AS (
  SELECT rowid FROM entries WHERE jyutping {operator} ?
),

matching_definition_ids AS (
  SELECT definition_id, definition FROM definitions WHERE fk_entry_id
    IN matching_entry_ids
),

matching_definitions AS (
  SELECT definition_id, fk_entry_id, fk_source_id, definition,
    label
  FROM definitions
  WHERE definitions.definition_id IN (
    SELECT definition_id FROM matching_definition_ids
  )
),

matching_definition_groups AS (
  SELECT fk_entry_id,
    json_object('source', sourcename,
                'definitions',
                json_group_array(json_object(
                  'definition', definition))) AS definitions
  FROM matching_definitions AS md
  LEFT JOIN sources ON sources.source_id = md.fk_source_id
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
        (query_param,),
    )

    records = c.fetchall()
    if not records:
        return None

    return query_utils.parse_returned_records(records)


def query_jyutping_exists(jyutping: str, fuzzy: bool) -> bool:
    db = get_db()
    c = db.cursor()

    query_param = query_utils.prepare_jyutping_bind_values(jyutping, fuzzy)

    if fuzzy:
        operator = REGEX_OPERATOR
    else:
        operator = GLOB_OPERATOR

    c.execute(
        f"""
SELECT EXISTS (
  SELECT
    rowid
  FROM entries
  WHERE jyutping {operator} ?
) AS existence
""",
        (query_param,),
    )

    records = c.fetchall()
    if not records:
        return None

    return query_utils.parse_existence(records)


def query_pinyin(pinyin: str, fuzzy: bool) -> list[Entry] | None:
    db = get_db()
    c = db.cursor()

    query_param = query_utils.prepare_pinyin_bind_values(pinyin, fuzzy)

    if fuzzy:
        operator = REGEX_OPERATOR
    else:
        operator = GLOB_OPERATOR

    c.execute(
        f"""
WITH matching_entry_ids AS (
  SELECT rowid FROM entries WHERE pinyin {operator} ?
),

matching_definition_ids AS (
  SELECT definition_id, definition FROM definitions WHERE fk_entry_id
    IN matching_entry_ids
),

matching_definitions AS (
  SELECT definition_id, fk_entry_id, fk_source_id, definition,
    label
  FROM definitions
  WHERE definitions.definition_id IN (
    SELECT definition_id FROM matching_definition_ids
  )
),

matching_definition_groups AS (
  SELECT fk_entry_id,
    json_object('source', sourcename,
                'definitions',
                json_group_array(json_object(
                  'definition', definition))) AS definitions
  FROM matching_definitions AS md
  LEFT JOIN sources ON sources.source_id = md.fk_source_id
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
        (query_param,),
    )

    records = c.fetchall()
    if not records:
        return None

    return query_utils.parse_returned_records(records)


def query_pinyin_exists(pinyin: str, fuzzy: bool) -> bool:
    db = get_db()
    c = db.cursor()

    query_param = query_utils.prepare_pinyin_bind_values(pinyin, fuzzy)

    if fuzzy:
        operator = REGEX_OPERATOR
    else:
        operator = GLOB_OPERATOR

    c.execute(
        f"""
SELECT EXISTS (
  SELECT
    rowid
  FROM entries
  WHERE pinyin {operator} ?
) AS existence
""",
        (query_param,),
    )

    records = c.fetchall()
    if not records:
        return None

    return query_utils.parse_existence(records)


def query_full_text(param: str) -> list[Entry] | None:
    db = get_db()
    c = db.cursor()

    # Exact match is specified by enclosing the query in double-quotes
    search_exact_match = len(param) >= 3 and param[0] == '"' and param[-1] == '"'

    if search_exact_match:
        # Remove the double-quotes and extra spaces
        param = " ".join(param[1:-1].split())
        like_param = param
    else:
        like_param = f"%{param}%"

    fts_param = f'"{param}"'

    c.execute(
        """
WITH matching_entry_ids AS (
  SELECT
    fk_entry_id,
    rowid AS definition_id,
    bm25(definitions_fts, 0, 1) AS RANK
  FROM definitions_fts
  WHERE definitions_fts MATCH ? AND definition LIKE ?
),

matching_definition_ids AS (
  SELECT
    definition_id,
    definition
  FROM definitions
  WHERE fk_entry_id IN (
    SELECT fk_entry_id
    FROM matching_entry_ids
  )
),

definitions_and_ranks AS (
  SELECT
    mdi.definition_id AS definition_id,
    mdi.definition AS definition,
    mei.rank AS RANK
  FROM matching_definition_ids AS mdi
    LEFT JOIN matching_entry_ids AS mei
      ON mdi.definition_id = mei.definition_id
),

matching_definitions AS (
  SELECT
    dar.definition_id,
    d.fk_entry_id,
    d.fk_source_id,
    d.definition,
    d.label,
    RANK
  FROM definitions_and_ranks AS dar
    JOIN definitions AS d
      ON dar.definition_id = d.definition_id
),

matching_definition_groups AS (
  SELECT fk_entry_id,
    CASE sourceshortname
      WHEN 'ABY' THEN AVG(md.rank) * 3
      WHEN 'CCY' THEN AVG(md.rank) * 3
      WHEN 'WHK' THEN AVG(md.rank) * 3
      WHEN 'YF' THEN AVG(md.rank) * 3
      ELSE AVG(md.rank)
    END AS RANK,
    json_object('source', sourcename,
                'definitions',
                json_group_array(json_object(
                  'definition', definition))) AS definitions
  FROM matching_definitions AS md
  LEFT JOIN sources ON sources.source_id = md.fk_source_id
  GROUP BY fk_entry_id, fk_source_id
),

matching_entries AS (
  SELECT
    simplified,
    traditional,
    jyutping,
    pinyin,
    SUM(RANK) AS RANK,
    json_group_array(json(definitions)) AS definitions
  FROM matching_definition_groups AS mdg
  LEFT JOIN entries ON entries.entry_id = mdg.fk_entry_id
  GROUP BY entry_id
  ORDER BY RANK ASC, frequency DESC
)

SELECT traditional, simplified, jyutping, pinyin, definitions FROM
  matching_entries
""",
        (
            fts_param,
            like_param,
        ),
    )

    records = c.fetchall()
    if not records:
        return None

    return query_utils.parse_returned_records(records)


def query_examples(param: str) -> list[SourceSentence] | None:
    db = get_db()
    c = db.cursor()

    like_param = f"%{param}%"

    c.execute(
        """
WITH
  matching_chinese_sentence_ids AS (
    SELECT chinese_sentence_id
    FROM chinese_sentences
    WHERE traditional LIKE ? ESCAPE '\\'
  ),
  translations_with_source AS (
    SELECT
      s.sourcename AS source,
      mcsi.chinese_sentence_id AS chinese_sentence_id,
      json_group_array(
        DISTINCT json_object(
          'sentence',
          sentence,
          'language',
          language,
          'direct',
          direct
        )
      ) AS translation
    FROM
      matching_chinese_sentence_ids AS mcsi
      LEFT JOIN sentence_links AS sl
        ON mcsi.chinese_sentence_id = sl.fk_chinese_sentence_id
      LEFT JOIN nonchinese_sentences AS ncs
        ON ncs.non_chinese_sentence_id = sl.fk_non_chinese_sentence_id
      LEFT JOIN sources AS s
        ON s.source_id = sl.fk_source_id
    GROUP BY s.sourcename, mcsi.chinese_sentence_id
  ),
  matching_translations AS (
    SELECT
      chinese_sentence_id,
      json_group_array(
        json_object(
          'source',
          source,
          'translations',
          json(translation)
        )
      ) AS translations
    FROM translations_with_source AS tws
    GROUP BY chinese_sentence_id
  ),
  matching_sentences AS (
    SELECT
      chinese_sentence_id,
      traditional,
      simplified,
      pinyin,
      jyutping,
      language
    FROM chinese_sentences AS cs
    WHERE
      chinese_sentence_id IN (
        SELECT chinese_sentence_id
        FROM matching_chinese_sentence_ids
      )
  ),
  matching_sentences_with_translations AS (
    SELECT
      max(sourcename) AS sourcename,
      traditional,
      simplified,
      pinyin,
      jyutping,
      language,
      translations
    FROM
      matching_sentences AS ms
      LEFT JOIN matching_translations AS mt
        ON ms.chinese_sentence_id = mt.chinese_sentence_id
      LEFT JOIN definitions_chinese_sentences_links AS dcsl
        ON ms.chinese_sentence_id = dcsl.fk_chinese_sentence_id
      LEFT JOIN definitions AS d
        ON dcsl.fk_definition_id = d.definition_id
      LEFT JOIN sources AS s ON d.fk_source_id = s.source_id
    GROUP BY
      traditional,
      simplified,
      pinyin,
      jyutping,
      language,
      translations
    ORDER BY ms.chinese_sentence_id
  )
SELECT
  sourcename,
  traditional,
  simplified,
  pinyin,
  jyutping,
  language,
  translations
FROM matching_sentences_with_translations
""",
        (like_param,),
    )

    records = c.fetchall()
    if not records:
        return None

    return query_utils.parse_returned_sentences(records)
