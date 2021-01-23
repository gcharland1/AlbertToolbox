import flask
import flask_sqlalchemy


app = flask.Flask(__name__)
app.config.from_object('config')

db = flask_sqlalchemy.SQLAlchemy(app)

@app.route('/home')
@app.route('/')
def home():
    return flask.render_template("index.html", title="Accueil")

@app.route('/tools')
def show_tools():
    return flask.render_template("our_tools.html", title="Nos outils")

@app.errorhandler(404)
def not_found(error):
    return flask.render_template("404.html", title="404 - Not found")

@app.errorhandler(500)
def internal_server_error(error):
    return flask.render_template("500.html", title="500 - Internal Server Error")


from app.authentification.controllers import auth
from app.tools.controllers import tools

app.register_blueprint(auth, url_prefix="/")
app.register_blueprint(tools, url_prefix="/")

db.create_all()