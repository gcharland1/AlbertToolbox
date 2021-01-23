import flask
import datetime
import flask_sqlalchemy

import forms
import piping_tools


app = flask.Flask(__name__)
app.register_blueprint(piping_tools.piping_tools, url_prefix="/")

app.permanent_session_lifetime = datetime.timedelta(minutes=5)
app.config['SECRET_KEY'] = '4b40c79de13feb562a644158dff8035c'
app.config['UPLOAD_PATH'] = "./upload/"
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = flask_sqlalchemy.SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(25))
    email = db.Column("email", db.String(100))
    password = db.Column("password", db.String(100))

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

@app.route('/home')
@app.route('/')
def home():
    return flask.render_template("index.html", title="Accueil")

@app.route('/register', methods=["GET", "POST"])
def register():
    if flask.request.method == "POST":

        username = flask.request.form['username']
        email = flask.request.form['email']
        password = flask.request.form['password']

        found_user = users.query.filter_by(email=email).first()
        if found_user:
            msg = 'Un compte existe déjà avec ce email. <a href="/login">Se connecter?</a>'
            url = "register"
        else:
            flask.session['user'] = username

            usr = users(username, email, password)
            db.session.add(usr)
            db.session.commit()

            flask.session.permanent = True
            msg = f"Connecté en tant que {username}"
            url = "home"

        flask.flash(flask.Markup(msg), "info")

        return flask.redirect(flask.url_for(url))
    else:
        form = forms.RegistrationForm()
        return flask.render_template("register.html", title="Register", form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    if flask.request.method == "POST":
        flask.session.permanent = True
        email = flask.request.form['email']
        password = flask.request.form['password']
        found_user = users.query.filter_by(email=email).first()
        if found_user:
            if found_user.password == password:
                username = found_user.name

                flask.session["user"] = username
                msg = f"Connecté en tant que {username}"
                url = "home"
            else:
                msg = "Mot de passe invalide"
                url = "login"
        else:
            msg = 'Aucun utilisateur avec cet email. <a href="/register">S''inscrire?</a>'
            url = "login"

        flask.flash(flask.Markup(msg), "info")
        return flask.redirect(flask.url_for(url))
    else:
        form = forms.LoginForm()
        return flask.render_template("login.html", title="Login", form=form)

@app.route('/logout')
def logout():
    if "user" in flask.session:
        flask.session.pop("user", None)
        flask.flash("Déconnecté avec succes", "info")

    return flask.redirect(flask.url_for("home"))

@app.route('/our_tools')
def show_tools():
    return flask.render_template("our_tools.html", title="Nos outils")


if __name__ == '__main__':
    db.create_all()
    app.run(host="0.0.0.0", port="8080", debug=True)
