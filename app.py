import os

from flask import Flask
from cantonais_org.dictionnaire.urls import dictionary_app

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['CANTONAIS_ORG_SECRET_KEY']

app.register_blueprint(dictionary_app, url_prefix="/dictionnaire")


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
