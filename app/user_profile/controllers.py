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
            update_db = False
            msg = None
            url = flask.url_for('user_profile.edit_profile')
            if hash_string(flask.request.form['old_password'], user.salt)[0] == user.password:
                new_username = flask.request.form['username']
                new_email = flask.request.form['email']
                new_password = flask.request.form['new_password']
                confirm_new_password = flask.request.form['confirm_new_password']

                if not new_username == user.name:
                    user.name = new_username
                    update_db = True

                if not new_email == user.email:
                    user.email = new_email
                    update_db = True

                if new_password:
                    if new_password == confirm_new_password:
                        user.password, user.salt = hash_string(flask.request.form['password'])
                        update_db = True
                    else:
                        msg = "Les nouveaux mots de passe ne sont pas identiques. "
                        msg += "Aucune donnée enregistré."
                        update_db = False


                if update_db:
                    db.session.commit()
                    msg = "Vos données ont été enregistré avec succès."
                    url = flask.url_for('user_profile.profile_page')

                    flask.session['user'] = new_username
                else:
                    if not msg:
                        msg = "Aucune modification apportée. Cliquez sur annuler pour revenir à votre profil."

            else:
                msg = "Votre mot de passe actuel est invalide. Aucun changement apporté à votre compte."

            if msg:
                flask.flash(msg, "info")
            return flask.redirect(url)

        else:
            return flask.render_template("user_profile/edit_profile.html", form=form, title=user.name, user=user)

    else:
        msg = f"Vous n'êtes pas connecté. <a href={flask.url_for('auth.login')}>Se connecter?</a>"
        url = 'main.home'

        flask.flash(flask.Markup(msg), 'info')
        return flask.redirect(flask.url_for(url))