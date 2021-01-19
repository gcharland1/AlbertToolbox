import flask
from forms import RegistrationForm, LoginForm

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = '4b40c79de13feb562a644158dff8035c'


@app.route('/')
def home():
    return flask.render_template("index.html")

@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    return flask.render_template("register.html", title="Register", form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    return flask.render_template("login.html", title="Login", form=form)

@app.route('/piping_estimator')
def get_cost():
    return flask.render_template("piping_estimator.html", title="Estimateur de coûts")

@app.route('/tools')
def show_tools():
    return flask.render_template("our_tools.html", title="Nos outils")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="8080", debug=True)
