from flask import render_template

from . import queries
from .utils import script_detector


def render_index(search_term="", search_type="search_auto"):
    return render_template(
        "dictionary_index.html", search_term=search_term, search_type=search_type
    )


def render_search_auto(search_term):
    if script_detector.contains_simplified_chinese(search_term):
        entries = queries.query_simplified(search_term)
    elif script_detector.contains_traditional_chinese(
        search_term
    ) or script_detector.contains_chinese(search_term):
        entries = queries.query_traditional(search_term)
    elif script_detector.is_valid_jyutping(
        search_term
    ) and queries.query_jyutping_exists(search_term):
        entries = queries.query_jyutping(search_term)
    elif script_detector.is_valid_pinyin(search_term) and queries.query_pinyin_exists(
        search_term
    ):
        entries = queries.query_pinyin(search_term)
    else:
        entries = queries.query_full_text(search_term)

    return render_template(
        "dictionary_search.html",
        search_term=search_term,
        search_type="search_auto",
        entries=entries,
    )


def render_search_traditional(search_term):
    entries = queries.query_traditional(search_term)
    return render_template(
        "dictionary_search.html",
        search_term=search_term,
        search_type="search_traditional",
        entries=entries,
    )


def render_search_simplified(search_term):
    entries = queries.query_simplified(search_term)
    return render_template(
        "dictionary_search.html",
        search_term=search_term,
        search_type="search_simplified",
        entries=entries,
    )


def render_search_jyutping(search_term):
    entries = queries.query_jyutping(search_term)
    return render_template(
        "dictionary_search.html",
        search_term=search_term,
        search_type="search_jyutping",
        entries=entries,
    )


def render_search_pinyin(search_term):
    entries = queries.query_pinyin(search_term)
    return render_template(
        "dictionary_search.html",
        search_term=search_term,
        search_type="search_pinyin",
        entries=entries,
    )


def render_search_french(search_term):
    entries = queries.query_full_text(search_term)
    return render_template(
        "dictionary_search.html",
        search_term=search_term,
        search_type="search_french",
        entries=entries,
    )


def render_entry(entry, search_term="", search_type="search_traditional"):
    entries = queries.get_traditional(entry)
    example_sample = queries.get_example_sample(entry)

    return render_template(
        "dictionary_entry.html",
        headword=entry,
        entries=entries,
        examples=example_sample,
        search_term=search_term,
        search_type=search_type,
    )
