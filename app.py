import os
import urllib.parse

from flask import Flask, g, render_template, redirect, request, url_for
from flask_babel import Babel, _, get_locale
from babel import Locale

try:
    # For Gunicorn
    from dictionnaire.urls import dictionary_app
except:
    # For local development
    from .dictionnaire.urls import dictionary_app

app = Flask(__name__)
app.config.from_object('cantonais_org.default_settings')
# app.config.from_envvar('CANTONAIS_ORG_SETTINGS')
babel = Babel(app)
app.config["SECRET_KEY"] = os.environ["CANTONAIS_ORG_SECRET_KEY"]

app.register_blueprint(dictionary_app, name="dictionnaire", url_prefix="/dictionnaire")
app.register_blueprint(dictionary_app, name="dictionary", url_prefix="/dictionary")

app.jinja_env.filters["quote"] = lambda x: urllib.parse.quote(x, safe="")


@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop("db", None)

    if db is not None:
        db.close()


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

    endpoint_name = _("dictionnaire") + f".{search_type}"
    return redirect(url_for(endpoint_name, search_term=search_term))


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        return redirect_post()

    search_term = request.cookies.get("search_term") or ""
    search_type = request.cookies.get("search_type") or ""

    return render_template(
        "index.html", search_term=search_term, search_type=search_type
    )


@app.route("/ressources", methods=["GET"])
@app.route("/resources", methods=["GET"])
def resources():
    if get_locale() == Locale("en"):
        return render_template(
            "resources.html"
        )
    else:
        return render_template(
            "ressources.html"
        )


@app.route("/telecharger", methods=["GET"])
@app.route("/download", methods=["GET"])
def download():
    if get_locale() == Locale("en"):
        return render_template(
            "download.html"
        )
    else:
        return render_template(
            "telecharger.html"
        )


@app.route("/a-propos", methods=["GET"])
@app.route("/about", methods=["GET"])
def about():
    if get_locale() == Locale("en"):
        return render_template(
            "a-propos.html"
        )
    else:
        return render_template(
            "about.html"
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0")
