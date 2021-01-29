import flask

from app import db
from app.authentification import forms
from app.authentification import user
from app.authentification import hash_string

auth = flask.Blueprint('auth', __name__)

@auth.route('/register', methods=["GET", "POST"])
def register():
    if flask.request.method == "POST":
        email = flask.request.form['email']
        found_user = user.query.filter_by(email=email).first()
        if found_user:
            msg = f'Un compte existe déjà avec ce email. <a href={flask.url_for("auth.login")}>Se connecter?</a>'
            url = "auth.register"
        else:
            username = flask.request.form['username']
            password, salt = hash_string(flask.request.form['password'])
            flask.session['user'] = username

            usr = user(username, email, password, salt)
            db.session.add(usr)
            db.session.commit()

            flask.session.permanent = True
            msg = f"Connecté en tant que {username}"
            url = "main.home"


        flask.flash(flask.Markup(msg), "info")

        return flask.redirect(flask.url_for(url))
    else:
        form = forms.RegistrationForm()
        return flask.render_template("auth/register.html", title="Register", form=form)

@auth.route('/login', methods=["GET", "POST"])
def login():
    if flask.request.method == "POST":
        email = flask.request.form['email']
        found_user = user.query.filter_by(email=email).first()
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
            msg = f'Aucun utilisateur avec cet email. <a href={flask.url_for("auth.register")}>S''inscrire?</a>'
            url = "auth.login"

        flask.flash(flask.Markup(msg), "info")
        return flask.redirect(flask.url_for(url))
    else:
        form = forms.LoginForm()
        return flask.render_template("auth/login.html", title="Login", form=form)

@auth.route('/logout')
def logout():
    if "user" in flask.session:
        flask.session.pop("user", None)
        flask.flash("Déconnecté avec succes", "info")

    return flask.redirect(flask.url_for("main.home"))
