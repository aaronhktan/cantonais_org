import os
import urllib.parse
import sqlite3

from flask import Flask, g, render_template, redirect, request, send_from_directory, url_for
from flask_babel import Babel, _, get_locale
from babel import Locale


def generate_sitemap(app):
    db = sqlite3.connect(app.config["DB_PATH"])
    c = db.cursor()
    c.execute("SELECT traditional FROM entries")

    records = c.fetchall()
    if not records:
        return

    sitemap_urls = []
    for i in range(0, len(records), 50000):
        # Sitemaps have a maximum of 50000 urls per file
        urls = []
        for j in range(i, min(i + 50000, len(records))):
            headword = urllib.parse.quote(records[j][0], safe="")
            if app.config["BABEL_DEFAULT_LOCALE"] == "en":
                urls.append(
                    f"{app.config["CANONICAL_URL"]}/dictionary/entry/{headword}")
            else:
                urls.append(
                    f"{app.config["CANONICAL_URL"]}/dictionnaire/entree/{headword}")

        with open(f"{os.getcwd()}/static/sitemap/sitemap{i // 50000}.txt", "w") as sitemap:
            sitemap.write("\n".join(urls))

        sitemap_urls.append(f"{app.config["CANONICAL_URL"]}/static/sitemap/sitemap{i // 50000}.txt")

    with open(f"{os.getcwd()}/static/robots/robots.txt", "w") as robots:
        for url in sitemap_urls:
            robots.write(f"Sitemap: {url}\n")


try:
    # For Gunicorn
    from dictionnaire.urls import dictionary_app
except:
    # For local development
    from .dictionnaire.urls import dictionary_app

app = Flask(__name__)
app.config.from_object('cantonais_org.default_settings')
babel = Babel(app)
app.config["SECRET_KEY"] = os.environ["CANTONAIS_ORG_SECRET_KEY"]
app.config["DB_PATH"] = os.environ["CANTONAIS_ORG_DB_PATH"]

app.register_blueprint(dictionary_app, name="dictionnaire", url_prefix="/dictionnaire")
app.register_blueprint(dictionary_app, name="dictionary", url_prefix="/dictionary")

app.jinja_env.filters["quote"] = lambda x: urllib.parse.quote(x, safe="")

generate_sitemap(app)


@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop("db", None)

    if db is not None:
        db.close()


@app.route('/robots.txt')
def static_from_root():
    return send_from_directory(f"{app.static_folder}/robots/", request.path[1:])


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

    endpoint_name = _("dictionnaire") + "./" + _("recherche") + f"/{search_type}"
    return redirect(url_for(endpoint_name, search_term=search_term))


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        return redirect_post()

    search_term = request.cookies.get("search_term") or ""
    search_type = request.cookies.get("search_type") or ""

    if get_locale() == Locale("en"):
        return render_template(
            "index_en.html"
        )
    else:
        return render_template(
            "index_fr.html", search_term=search_term, search_type=search_type
        )


@app.route("/ressources", endpoint="ressources", methods=["GET"])
@app.route("/resources", endpoint="resources", methods=["GET"])
def resources():
    if get_locale() == Locale("en"):
        return render_template(
            "resources.html"
        )
    else:
        return render_template(
            "ressources.html"
        )


@app.route("/telecharger", endpoint="telecharger", methods=["GET"])
@app.route("/download", endpoint="download", methods=["GET"])
def download():
    if get_locale() == Locale("en"):
        return redirect(url_for("index") + "#download-program")
    else:
        return render_template(
            "telecharger.html"
        )


@app.route("/a-propos", endpoint="a-propos", methods=["GET"])
@app.route("/about", endpoint="about", methods=["GET"])
def about():
    if get_locale() == Locale("en"):
        return render_template(
            "about.html"
        )
    else:
        return render_template(
            "a-propos.html"
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0")
