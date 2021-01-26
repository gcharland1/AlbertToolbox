import flask
import flask_sqlalchemy


app = flask.Flask(__name__)
app.config.from_object('config')

db = flask_sqlalchemy.SQLAlchemy(app)

@app.errorhandler(404)
def not_found(error):
    return flask.render_template("404.html", title="404 - Not found")


from app.main.controllers import main
from app.authentification.controllers import auth
from app.tools.controllers import tools

app.register_blueprint(main, url_prefix="/")
app.register_blueprint(auth, url_prefix="/")
app.register_blueprint(tools, url_prefix="/")

db.create_all()