import flask
import os

from app import db
from app.authentification import forms
from app.authentification import user

main = flask.Blueprint('main', __name__, )

@main.route('/accueil')
@main.route('/main')
@main.route('/')
def home():

    return flask.render_template("index.html", title="Accueil")

@main.route('/tools')
def show_tools():
    return flask.render_template("our_tools.html", title="Nos outils")
