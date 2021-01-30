import flask

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
            salt = found_user.salt
            password, _ = hash_string(flask.request.form['password'], salt)
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

@auth.route('/reset_password', methods=["GET", "POST"])
def reset_password():
    if flask.request.method == "POST":
        email = flask.request.form['email']
        found_user = User.query.filter_by(email=email).first()
        if found_user:
            username = found_user.name

            temp_link = get_random_string(16)
            found_user.temp_link = temp_link


            msg_link = flask.url_for("main.home") + username + "/" + temp_link

            if mail_service.reset_password(email, username, msg_link):
                msg = f"Un mot de passe temporaire a été envoyé à {email}. " + \
                              "Ce nouveau mot de passe est valide pour une durée de 5 min."
                url = "main.home"
            else:
                msg = "Une erreur est survenue. Veuillez réessayer plus tard."
                url = "auth.login"
        else:
            msg = f'Aucun utilisateur correspond à cet email. <a href={flask.url_for("auth.register")}>S''inscrire?</a>'
            url = "auth.reset_password"

        flask.flash(flask.Markup(msg), "info")
        return flask.redirect(flask.url_for(url))
    else:
        form = forms.ResetForm()
        return flask.render_template("auth/reset_password.html", title="Mot de passe oublié", form=form)



@auth.route('/logout')
def logout():
    if "user" in flask.session:
        flask.session.pop("user", None)
        flask.flash("Déconnecté avec succes", "info")

    return flask.redirect(flask.url_for("main.home"))
