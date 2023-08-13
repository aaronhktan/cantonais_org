import os

from flask import Flask, g
from cantonais_org.dictionnaire.urls import dictionary_app

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['CANTONAIS_ORG_SECRET_KEY']

app.register_blueprint(dictionary_app, url_prefix="/dictionnaire")


@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)

    if db is not None:
        db.close()


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
