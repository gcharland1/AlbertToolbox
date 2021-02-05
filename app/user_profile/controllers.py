import flask

from app.user_profile import forms

user_profile = flask.Blueprint('user_profile', __name__)

@user_profile.route('/')
def profile_page():
    if 'user' in flask.session:
        username = flask.session['user']
        return f"Success! {username}"
    else:
        msg = f"Vous n'êtes pas connecter. <a href={flask.url_for('auth.login')}>Se connecter?</a>"
        url = 'main.home'

        flask.flash(flask.Markup(msg), 'info')
        return flask.redirect(flask.url_for(url))