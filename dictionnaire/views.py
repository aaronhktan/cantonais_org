from flask import render_template, request, redirect, url_for

from .queries import *


def render_index():
    return render_template("index.html")


def render_search_traditional(search_term):
    entry = query_traditional(search_term)
    return render_template("search.html", search_term=search_term, search_type="search_traditional", entry=entry)


def render_search_simplified(search_term):
    return render_template("search.html", search_term=search_term, search_type="search_simplified")


def render_search_jyutping(search_term):
    return render_template("search.html", search_term=search_term, search_type="search_jyutping")


def render_search_pinyin(search_term):
    return render_template("search.html", search_term=search_term, search_type="search_pinyin")


def render_search_french(search_term):
    return render_template("search.html", search_term=search_term, search_type="search_french")


def render_entry(search_term):
    return f"entrée {search_term}"
