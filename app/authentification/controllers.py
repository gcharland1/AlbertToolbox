import flask

from app import app
from app import db
from app import mail_service

from app.authentification import forms
from app.authentification import User
from app.authentification import hash_string, get_random_string


auth = flask.Blueprint('auth', __name__)

@auth.route('/register', methods=["GET", "POST"])
def register():
    if flask.request.method == "POST":
        email = flask.request.form['email']
        found_user = User.query.filter_by(email=email).first()
        if found_user:
            msg = f'Un compte existe déjà avec ce email. <a href={flask.url_for("auth.login")}>Se connecter?</a>'
            url = "auth.register"
        else:
            username = flask.request.form['username']
            password, salt = hash_string(flask.request.form['password'])
            flask.session['user'] = username

            usr = User(username, email, password, salt)
            db.session.add(usr)
            db.session.commit()

            flask.session.permanent = True
            msg = f"Connecté en tant que {username}"
            url = "main.home"


        flask.flash(flask.Markup(msg), "info")

        return flask.redirect(flask.url_for(url))
    else:
        form = forms.RegistrationForm()
        return flask.render_template("auth/register.html", title="S'inscrire", form=form)

@auth.route('/login', methods=["GET", "POST"])
def login():
    if flask.request.method == "POST":
        email = flask.request.form['email']
        found_user = User.query.filter_by(email=email).first()
        if found_user:
            password, _ = hash_string(flask.request.form['password'], found_user.salt)
            if found_user.password == password:
                username = found_user.name
                flask.session["user"] = username
                flask.session.permanent = True
                msg = f"Connecté en tant que {username}"
                url = "main.home"
            else:
                msg = "Mot de passe invalide"
                url = "auth.login"
        else:
            msg = f'Aucun utilisateur correspond à cet email. <a href={flask.url_for("auth.register")}>S''inscrire?</a>'
            url = "auth.login"

        flask.flash(flask.Markup(msg), "info")
        return flask.redirect(flask.url_for(url))
    else:
        form = forms.LoginForm()
        return flask.render_template("auth/login.html", title="Connection", form=form)

@auth.route('/forgot_password', methods=["GET", "POST"])
def forgot_password():
    if flask.request.method == "POST":
        email = flask.request.form['email']
        found_user = User.query.filter_by(email=email).first()
        if found_user:
            username = found_user.name

            tmp_link = get_random_string(16)
            found_user.tmp_link = tmp_link
            db.session.commit()

            msg_link = app.config["SERVER_NAME"] + "/" + username + "/" + tmp_link

            if mail_service.reset_password(email, username, msg_link):
                msg = f"Un lien pour réinitialiser votre mot de passe a été envoyé à {email}. "
                url = "main.home"
            else:
                msg = "Une erreur est survenue. Veuillez réessayer plus tard."
                url = "auth.login"
        else:
            msg = f'Aucun utilisateur correspond à cet email. <a href={flask.url_for("auth.register")}>S''inscrire?</a>'
            url = "auth.forgot_password"

        flask.flash(flask.Markup(msg), "info")
        return flask.redirect(flask.url_for(url))
    else:
        form = forms.ForgotPasswordForm()
        return flask.render_template("auth/forgot_password.html", title="Mot de passe oublié", form=form)

@auth.route('/<username>/<tmp_link>', methods=["GET", "POST"])
def reset_password(username, tmp_link):
    found_user = User.query.filter_by(name=username).first()
    if found_user:
        if found_user.tmp_link == tmp_link:
            if flask.request.method == "POST":
                password, salt = hash_string(flask.request.form['password'])
                found_user.password = password
                found_user.salt = salt
                found_user.tmp_link = ""

                db.session.commit()

                flask.session['user'] = found_user.name
                msg = "Mot de passe changé avec succès!"
                url = "main.home"
            else:
                form = forms.ResetPasswordForm()
                return flask.render_template("auth/reset_password.html", title="Changer de mot de passe", form=form)
        else:
            msg = "Le lien utilié est expiré ou invalide. Veuillez valider que vous avez bien utilisé le plus récent ou "
            msg += f'<a href={flask.url_for("auth.forgot_password")}>envoyer à nouveau</a>.'
            url = "main.home"

        flask.flash(flask.Markup(msg), "info")
        return flask.redirect(flask.url_for(url))


@auth.route('/logout')
def logout():
    if "user" in flask.session:
        flask.session.pop("user", None)
        flask.flash("Déconnecté avec succès", "info")

    return flask.redirect(flask.url_for("main.home"))
