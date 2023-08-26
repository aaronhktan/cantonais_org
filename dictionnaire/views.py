from flask import render_template

from . import queries


def render_index():
    return render_template("index.html")


def render_search_traditional(search_term):
    entries = queries.query_traditional(search_term)
    return render_template("search.html", search_term=search_term,
                           search_type="search_traditional", entries=entries)


def render_search_simplified(search_term):
    entries = queries.query_simplified(search_term)
    return render_template("search.html", search_term=search_term,
                           search_type="search_simplified", entries=entries)


def render_search_jyutping(search_term):
    entries = queries.query_jyutping(search_term)
    return render_template("search.html", search_term=search_term,
                           search_type="search_jyutping", entries=entries)


def render_search_pinyin(search_term):
    entries = queries.query_pinyin(search_term)
    return render_template("search.html", search_term=search_term,
                           search_type="search_pinyin", entries=entries)


def render_search_french(search_term):
    entries = queries.query_full_text(search_term)
    return render_template("search.html", search_term=search_term,
                           search_type="search_french", entries=entries)


def render_entry(entry, search_term="", search_type="search_traditional"):
    record = queries.get_traditional(entry)
    return render_template("entry.html", entry=record,
                           search_term=search_term, search_type=search_type)
