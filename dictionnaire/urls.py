from flask import Blueprint
from .views import *

dictionary_app = Blueprint('dictionary_app', __name__, static_folder="static",
                           static_url_path="dictionnaire/static", template_folder="templates")


def redirect_post():
    if "search_term" in request.form:
        search_term = request.form['search_term']
    else:
        search_term = request.form['search_term_mobile']
    if "search_type" in request.form:
        search_type = request.form['search_type']
    else:
        search_type = request.form['search_type_mobile']
    return redirect(url_for(f'dictionary_app.{search_type}', search_term=search_term))


@dictionary_app.route("/", methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        return redirect_post()
    return render_index()


@dictionary_app.route("/recherche/traditionnel/<search_term>", methods=('GET', 'POST'))
def search_traditional(search_term):
    if request.method == 'POST':
        return redirect_post()
    return render_search_traditional(search_term)


@dictionary_app.route("/recherche/simplifie/<search_term>", methods=('GET', 'POST'))
def search_simplified(search_term):
    if request.method == 'POST':
        return redirect_post()
    return render_search_simplified(search_term)


@dictionary_app.route("/recherche/jyutping/<search_term>", methods=('GET', 'POST'))
def search_jyutping(search_term):
    if request.method == 'POST':
        return redirect_post()
    return render_search_jyutping(search_term)


@dictionary_app.route("/recherche/pinyin/<search_term>", methods=('GET', 'POST'))
def search_pinyin(search_term):
    if request.method == 'POST':
        return redirect_post()
    return render_search_pinyin(search_term)


@dictionary_app.route("/recherche/fr/<search_term>", methods=('GET', 'POST'))
def search_french(search_term):
    if request.method == 'POST':
        return redirect_post()
    return render_search_french(search_term)


@dictionary_app.route("/entree/<entry>", methods=('GET', 'POST'))
def entry_view(entry):
    if request.method == 'POST':
        return redirect_post()
    return render_entry(entry)
