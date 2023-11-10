import os

from flask import Flask, g, render_template, redirect, request, url_for
try:
    # For Gunicorn
    from dictionnaire.urls import dictionary_app
except:
    # For local development
    from .dictionnaire.urls import dictionary_app

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ["CANTONAIS_ORG_SECRET_KEY"]

app.register_blueprint(dictionary_app, url_prefix="/dictionnaire")


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

    print("hi!")

    return redirect(url_for(f"dictionary_app.{search_type}",
                            search_term=search_term))


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        return redirect_post()

    search_term = request.cookies.get("search_term") or ""
    search_type = request.cookies.get("search_type") or ""

    return render_template("index.html", search_term=search_term,
                           search_type=search_type)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
