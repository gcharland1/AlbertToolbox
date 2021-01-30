import flask
import flask_sqlalchemy
import flask_mail

class ColorScheme:
    backgrounds_green = ["#BAC7BE", "#C2E1C2", "#7DCD85", "#80AB82", "#778472"]
    backgrounds_gray  = ["#F4F3EE", "#BCB8B1", "#8A817C",]
    pass

app = flask.Flask(__name__)
app.config.from_object('config')

db = flask_sqlalchemy.SQLAlchemy(app)
mail = flask_mail.Mail(app)

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