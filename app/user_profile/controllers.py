import flask
from app import db
from app.authentification import User, hash_string
from app.user_profile import forms

user_profile = flask.Blueprint('user_profile', __name__)

@user_profile.route('/')
def profile_page():
    if 'user' in flask.session:
        username = flask.session['user']
        user = User.query.filter_by(name=username).first()

        return flask.render_template("user_profile/profile_page.html", title=user.name, user=user)
    else:
        msg = f"Vous n'êtes pas connecté. <a href={flask.url_for('auth.login')}>Se connecter?</a>"
        url = 'main.home'

        flask.flash(flask.Markup(msg), 'info')
        return flask.redirect(flask.url_for(url))

@user_profile.route("/edit", methods=["GET", "POST"])
def edit_profile():
    if 'user' in flask.session:
        username = flask.session['user']
        user = User.query.filter_by(name=username).first()
        form = forms.EditProfileFrom()
        if flask.request.method == "POST":
            msg = ""
            update_db = False
            if form.cancel.data:
                msg += "Modifications annulées avec succès"
            else:
                if form.new_password.data:
                    new_password = flask.request.form['new_password']
                    confirm_new_password = flask.request.form['confirm_new_password']
                    if new_password == confirm_new_password:
                        user.password, user.salt = hash_string(flask.request.form['password'])
                    else:
                        msg += "Les mots de passe ne sont pas identiques"
            url = flask.url_for('user_profile.profile_page')
            flask.flash(msg, "info")
            return flask.redirect(url)
        else:
            return flask.render_template("user_profile/edit_profile.html", form=form, title=user.name, user=user)
    else:
        msg = f"Vous n'êtes pas connecté. <a href={flask.url_for('auth.login')}>Se connecter?</a>"
        url = 'main.home'

        flask.flash(flask.Markup(msg), 'info')
        return flask.redirect(flask.url_for(url))