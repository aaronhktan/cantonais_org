from flask import render_template
from flask_babel import _, pgettext

from . import queries
from .utils import script_detector


def render_index(search_term="", search_type="search_auto"):
    return render_template(
        "dictionary_index.html", search_term=search_term, search_type=search_type
    )


def render_search_auto(search_term):
    if script_detector.contains_simplified_chinese(search_term):
        entries = queries.query_simplified(search_term)
        detected_search_type = _("caractères simplifiés")
    elif script_detector.contains_traditional_chinese(
        search_term
    ) or script_detector.contains_chinese(search_term):
        entries = queries.query_traditional(search_term)
        detected_search_type = _("caractères traditionnels")
    elif queries.query_jyutping_exists(search_term, fuzzy=False):
        entries = queries.query_jyutping(search_term, fuzzy=False)
        detected_search_type = _("Jyutping")
    elif queries.query_jyutping_exists(search_term, fuzzy=True):
        entries = queries.query_jyutping(search_term, fuzzy=True)
        detected_search_type = pgettext("views.py", "Jyutping approximatif")
    elif queries.query_pinyin_exists(search_term):
        entries = queries.query_pinyin(search_term)
        detected_search_type = _("Pinyin")
    else:
        entries = queries.query_full_text(search_term)
        detected_search_type = _("français")

    return render_template(
        "dictionary_search.html",
        search_term=search_term,
        search_type=_("auto"),
        detected_search_type=detected_search_type,
        entries=entries,
    )


def render_search_traditional(search_term):
    entries = queries.query_traditional(search_term)
    return render_template(
        "dictionary_search.html",
        search_term=search_term,
        search_type=_("traditionnel"),
        entries=entries,
    )


def render_search_simplified(search_term):
    entries = queries.query_simplified(search_term)
    return render_template(
        "dictionary_search.html",
        search_term=search_term,
        search_type=_("simplifie"),
        entries=entries,
    )


def render_search_jyutping(search_term: str, fuzzy: bool) -> str:
    entries = queries.query_jyutping(search_term, fuzzy)
    search_type = _("fuzzy-jyutping") if fuzzy else _("jyutping")
    return render_template(
        "dictionary_search.html",
        search_term=search_term,
        search_type=search_type,
        entries=entries,
    )


def render_search_pinyin(search_term):
    entries = queries.query_pinyin(search_term)
    return render_template(
        "dictionary_search.html",
        search_term=search_term,
        search_type=_("pinyin"),
        entries=entries,
    )


def render_search_french(search_term):
    entries = queries.query_full_text(search_term)
    return render_template(
        "dictionary_search.html",
        search_term=search_term,
        search_type=_("fr"),
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
