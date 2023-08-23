from flask import render_template

from . import queries


def render_index():
    return render_template("index.html")


def render_search_traditional(search_term):
    entry = queries.query_traditional(search_term)
    return render_template("search.html", search_term=search_term,
                           search_type="search_traditional", entry=entry)


def render_search_simplified(search_term):
    entry = queries.query_simplified(search_term)
    return render_template("search.html", search_term=search_term,
                           search_type="search_simplified", entry=entry)


def render_search_jyutping(search_term):
    entry = queries.query_jyutping(search_term)
    return render_template("search.html", search_term=search_term,
                           search_type="search_jyutping", entry=entry)


def render_search_pinyin(search_term):
    return render_template("search.html", search_term=search_term,
                           search_type="search_pinyin")


def render_search_french(search_term):
    return render_template("search.html", search_term=search_term,
                           search_type="search_french")


def render_entry(entry, search_term="", search_type="search_traditional"):
    record = queries.get_traditional(entry)
    return render_template("entry.html", entry=record,
                           search_term=search_term, search_type=search_type)
