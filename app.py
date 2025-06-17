import os
import urllib.parse
import sqlite3
import xml.etree.ElementTree as ET

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
    for i in range(0, len(records), 10000):
        # Sitemaps have a maximum of 50000 urls per file
        root_elem = ET.Element("urlset")
        root_elem.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")

        for j in range(i, min(i + 10000, len(records))):
            headword = urllib.parse.quote(records[j][0], safe="")

            url_elem = ET.SubElement(root_elem, "url")
            loc_elem = ET.SubElement(url_elem, "loc")
            if app.config["BABEL_DEFAULT_LOCALE"] == "en":
                loc_elem.text = f"{app.config["CANONICAL_URL"]}/dictionary/entry/{headword}"
            else:
                loc_elem.text = f"{app.config["CANONICAL_URL"]}/dictionnaire/entree/{headword}"

        tree = ET.ElementTree(root_elem)
        tree.write(f"{os.getcwd()}/static/sitemap/sitemap{i // 10000}.xml", encoding="utf-8", xml_declaration=True)
        sitemap_urls.append(f"{app.config["CANONICAL_URL"]}/sitemap{i // 10000}.xml")

    root_elem = ET.Element("sitemapindex")
    root_elem.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")
    for url in sitemap_urls:
        sitemap_elem = ET.SubElement(root_elem, "sitemap")
        loc_elem = ET.SubElement(sitemap_elem, "loc")
        loc_elem.text = url
    tree = ET.ElementTree(root_elem)
    tree.write(f"{os.getcwd()}/static/sitemap/sitemap_index.xml", encoding="utf-8", xml_declaration=True)

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
app.jinja_env.filters["log"] = lambda x: print(x)

generate_sitemap(app)


@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop("db", None)

    if db is not None:
        db.close()


@app.route('/robots.txt')
def robot_from_root():
    return send_from_directory(f"{app.static_folder}/robots/", request.path[1:])

@app.route('/sitemap_index.xml')
@app.route('/sitemap<sitemap_num>.xml')
def sitemap_from_root(sitemap_num=None):
    return send_from_directory(f"{app.static_folder}/sitemap/", request.path[1:])


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
