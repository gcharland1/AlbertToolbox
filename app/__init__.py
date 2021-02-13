import flask
import flask_sqlalchemy
import flask_mail
import os

class ColorScheme:
    backgrounds_green = ["#BAC7BE", "#C2E1C2", "#7DCD85", "#80AB82", "#778472"]
    backgrounds_gray  = ["#F4F3EE", "#BCB8B1", "#8A817C"]
    pass

app = flask.Flask(__name__)
app.config.from_object('config')

db = flask_sqlalchemy.SQLAlchemy(app)
mail = flask_mail.Mail(app)

@app.errorhandler(404)
def not_found(error):
    return flask.render_template("error_handling/404.html", title="404 - Not found"),404

@app.errorhandler(500)
def internal_error(error):
    return flask.render_template("error_handling/500.html", title="500 - Internal error"),500

from app.main.controllers import main
from app.authentification.controllers import auth
from app.piping_estimator.controllers import tools

app.register_blueprint(main, url_prefix="/")
app.register_blueprint(auth, url_prefix="/")
app.register_blueprint(tools, url_prefix="/")

db.create_all()