import flask
from app import db
from app.authentification import User
from app.user_profile import forms

user_profile = flask.Blueprint('user_profile', __name__)

@user_profile.route('/')
def profile_page():
    if 'user' in flask.session:
        username = flask.session['user']
        user = User.query.filter_by(name=username).first()

        return flask.render_template("user_profile/profile_page.html", user=user)
    else:
        msg = f"Vous n'êtes pas connecté. <a href={flask.url_for('auth.login')}>Se connecter?</a>"
        url = 'main.home'

        flask.flash(flask.Markup(msg), 'info')
        return flask.redirect(flask.url_for(url))