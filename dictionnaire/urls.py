from flask import Blueprint, make_response, request, redirect, url_for
from flask_babel import _
from . import views

import urllib.parse

dictionary_app = Blueprint(
    "dictionary_app",
    __name__,
    static_folder="static",
    static_url_path="dictionnaire/static",
    template_folder="templates",
)


def redirect_post():
    if "search_term" in request.form:
        search_term = request.form["search_term"]
    else:
        search_term = request.form["search_term_mobile"]
    if "search_type" in request.form:
        search_type = request.form["search_type"]
    else:
        search_type = request.form["search_type_mobile"]

    # Remove whitespace surrounding the search term
    search_term = search_term.strip()
    search_term = urllib.parse.quote(search_term, safe="")

    endpoint_name = _("dictionnaire./recherche") + f"/{search_type}"
    return redirect(url_for(endpoint_name, search_term=search_term))


@dictionary_app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        return redirect_post()

    search_term = request.cookies.get("search_term") or ""
    search_type = request.cookies.get("search_type") or ""

    resp = make_response(views.render_index(search_term, search_type))

    return resp


@dictionary_app.route("/recherche/auto/<search_term>", endpoint="/recherche/auto", methods=("GET", "POST"))
@dictionary_app.route("/search/auto/<search_term>", endpoint="/search/auto", methods=("GET", "POST"))
def search_auto(search_term):
    if request.method == "POST":
        return redirect_post()

    search_term = urllib.parse.unquote(search_term)

    resp = make_response(views.render_search_auto(search_term))

    resp.set_cookie("search_term", search_term)
    resp.set_cookie("search_type", _("auto"))

    return resp


@dictionary_app.route("/recherche/traditionnel/<search_term>", endpoint="/recherche/traditionnel", methods=("GET", "POST"))
@dictionary_app.route("/search/traditional/<search_term>", endpoint="/search/traditional", methods=("GET", "POST"))
def search_traditional(search_term):
    if request.method == "POST":
        return redirect_post()

    search_term = urllib.parse.unquote(search_term)

    resp = make_response(views.render_search_traditional(search_term))

    resp.set_cookie("search_term", search_term)
    resp.set_cookie("search_type", _("traditionnel"))

    return resp


@dictionary_app.route("/recherche/simplifie/<search_term>", endpoint="/recherche/simplifie", methods=("GET", "POST"))
@dictionary_app.route("/search/simplified/<search_term>", endpoint="/search/simplified", methods=("GET", "POST"))
def search_simplified(search_term):
    if request.method == "POST":
        return redirect_post()

    search_term = urllib.parse.unquote(search_term)

    resp = make_response(views.render_search_simplified(search_term))

    resp.set_cookie("search_term", search_term)
    resp.set_cookie("search_type", _("simplifie"))

    return resp


@dictionary_app.route("/recherche/jyutping/<search_term>", endpoint="/recherche/jyutping", methods=("GET", "POST"))
@dictionary_app.route("/search/jyutping/<search_term>", endpoint="/search/jyutping", methods=("GET", "POST"))
def search_jyutping(search_term):
    if request.method == "POST":
        return redirect_post()

    search_term = urllib.parse.unquote(search_term)

    resp = make_response(views.render_search_jyutping(search_term))

    resp.set_cookie("search_term", search_term)
    resp.set_cookie("search_type", _("jyutping"))

    return resp


@dictionary_app.route("/recherche/pinyin/<search_term>", endpoint="/recherche/pinyin", methods=("GET", "POST"))
@dictionary_app.route("/search/pinyin/<search_term>", endpoint="/search/pinyin", methods=("GET", "POST"))
def search_pinyin(search_term):
    if request.method == "POST":
        return redirect_post()

    search_term = urllib.parse.unquote(search_term)

    resp = make_response(views.render_search_pinyin(search_term))

    resp.set_cookie("search_term", search_term)
    resp.set_cookie("search_type", _("pinyin"))

    return resp


@dictionary_app.route("/recherche/fr/<search_term>", endpoint="/recherche/fr", methods=("GET", "POST"))
@dictionary_app.route("/search/en/<search_term>", endpoint="/search/en", methods=("GET", "POST"))
def search_french(search_term):
    if request.method == "POST":
        return redirect_post()

    search_term = urllib.parse.unquote(search_term)

    resp = make_response(views.render_search_french(search_term))

    resp.set_cookie("search_term", search_term)
    resp.set_cookie("search_type", _("fr"))

    return resp


@dictionary_app.route("/entree/<entry>", endpoint="/entree", methods=("GET", "POST"))
@dictionary_app.route("/entry/<entry>", endpoint="/entry", methods=("GET", "POST"))
def entry_view(entry):
    if request.method == "POST":
        return redirect_post()

    entry = urllib.parse.unquote(entry)

    search_term = request.cookies.get("search_term") or ""
    search_type = request.cookies.get("search_type") or ""

    return views.render_entry(entry, search_term, search_type)
