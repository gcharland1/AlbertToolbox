import flask
import forms
import datetime
import os
import image_reader



app = flask.Flask(__name__)
app.config['SECRET_KEY'] = '4b40c79de13feb562a644158dff8035c'
app.config['UPLOAD PATH'] = "./upload/"
app.permanent_session_lifetime = datetime.timedelta(minutes=5)


@app.route('/<name>')
def name(name):
    return name

@app.route('/')
def home():
    return flask.render_template("index.html", title="Accueil")

@app.route('/user')
def user():
    if "email" in flask.session:
        name = flask.session["email"]
        return f"<h1>{name}</h1>"
    else:
        return flask.redirect(flask.url_for("login"))


@app.route('/register', methods=["GET", "POST"])
def register():
    if flask.request.method == "POST":
        flask.session.permanent = True
        flask.session['email'] = flask.request.form['email']
        return flask.redirect(flask.url_for(user))
    else:
        form = forms.RegistrationForm()
        return flask.render_template("register.html", title="Register", form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    if flask.request.method == "POST":
        flask.session.permanent = True
        flask.session['email'] = flask.request.form['email']
        return flask.redirect(flask.url_for("user"))
    else:
        form = forms.LoginForm()
        return flask.render_template("login.html", title="Login", form=form)

@app.route('/logout')
def logout():
    flask.session.pop("email", None)
    return flask.redirect(flask.url_for("home"))

@app.route('/piping_estimator', methods=["GET", "POST"])
def get_cost():
    form = forms.PipingForm()
    if flask.request.method == 'POST':
        filename = form.file.data.filename
        print(filename)
        file_data = flask.request.files[form.file.name].read()

        open(os.path.join(app.config["UPLOAD PATH"], filename), 'wb').write(file_data)

        return flask.redirect(flask.url_for('name', name="succes"))

    else:
        return flask.render_template("piping_estimator.html", title="Estimateur de coûts", form=form)

@app.route('/tools')
def show_tools():
    return flask.render_template("our_tools.html", title="Nos outils")



if __name__ == '__main__':
    app.run(host="0.0.0.0", port="8080", debug=True)
