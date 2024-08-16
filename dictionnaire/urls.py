from flask import Blueprint, make_response, request, redirect, url_for
from . import views

import urllib.parse

dictionary_app = Blueprint("dictionary_app", __name__, static_folder="static",
                           static_url_path="dictionnaire/static",
                           template_folder="templates")


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

    return redirect(url_for(f"dictionary_app.{search_type}",
                            search_term=search_term))


@dictionary_app.route("/ressources", methods=("GET", "POST"))
def resources():
    if request.method == "POST":
        return redirect_post()

    search_term = request.cookies.get("search_term") or ""
    search_type = request.cookies.get("search_type") or ""

    return views.render_index(search_term, search_type)


@dictionary_app.route("/telecharger", methods=("GET", "POST"))
def download():
    if request.method == "POST":
        return redirect_post()

    search_term = request.cookies.get("search_term") or ""
    search_type = request.cookies.get("search_type") or ""

    return views.render_index(search_term, search_type)


@dictionary_app.route("/a-propos", methods=("GET", "POST"))
def about():
    if request.method == "POST":
        return redirect_post()

    search_term = request.cookies.get("search_term") or ""
    search_type = request.cookies.get("search_type") or ""

    return views.render_index(search_term, search_type)


@dictionary_app.route("/recherche/auto/<search_term>",
                      methods=("GET", "POST"))
def search_auto(search_term):
    if request.method == "POST":
        return redirect_post()

    search_term = urllib.parse.unquote(search_term)

    resp = make_response(views.render_search_auto(search_term))

    resp.set_cookie("search_term", search_term)
    resp.set_cookie("search_type", search_auto.__name__)

    return resp


@dictionary_app.route("/recherche/traditionnel/<search_term>",
                      methods=("GET", "POST"))
def search_traditional(search_term):
    if request.method == "POST":
        return redirect_post()

    search_term = urllib.parse.unquote(search_term)

    resp = make_response(views.render_search_traditional(search_term))

    resp.set_cookie("search_term", search_term)
    resp.set_cookie("search_type", search_traditional.__name__)

    return resp


@dictionary_app.route("/recherche/simplifie/<search_term>",
                      methods=("GET", "POST"))
def search_simplified(search_term):
    if request.method == "POST":
        return redirect_post()

    search_term = urllib.parse.unquote(search_term)

    resp = make_response(views.render_search_simplified(search_term))

    resp.set_cookie("search_term", search_term)
    resp.set_cookie("search_type", search_simplified.__name__)

    return resp


@dictionary_app.route("/recherche/jyutping/<search_term>",
                      methods=("GET", "POST"))
def search_jyutping(search_term):
    if request.method == "POST":
        return redirect_post()

    search_term = urllib.parse.unquote(search_term)

    resp = make_response(views.render_search_jyutping(search_term))

    resp.set_cookie("search_term", search_term)
    resp.set_cookie("search_type", search_jyutping.__name__)

    return resp


@dictionary_app.route("/recherche/pinyin/<search_term>",
                      methods=("GET", "POST"))
def search_pinyin(search_term):
    if request.method == "POST":
        return redirect_post()

    search_term = urllib.parse.unquote(search_term)

    resp = make_response(views.render_search_pinyin(search_term))

    resp.set_cookie("search_term", search_term)
    resp.set_cookie("search_type", search_pinyin.__name__)

    return resp


@dictionary_app.route("/recherche/fr/<search_term>",
                      methods=("GET", "POST"))
def search_french(search_term):
    if request.method == "POST":
        return redirect_post()

    search_term = urllib.parse.unquote(search_term)

    resp = make_response(views.render_search_french(search_term))

    resp.set_cookie("search_term", search_term)
    resp.set_cookie("search_type", search_french.__name__)

    return resp


@dictionary_app.route("/entree/<entry>",
                      methods=("GET", "POST"))
def entry_view(entry):
    if request.method == "POST":
        return redirect_post()

    entry = urllib.parse.unquote(entry)

    search_term = request.cookies.get("search_term") or ""
    search_type = request.cookies.get("search_type") or ""

    return views.render_entry(entry, search_term, search_type)
