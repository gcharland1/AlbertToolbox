import flask
app = flask.Flask(__name__)


@app.route('/')
def home():
    return flask.render_template("index.html")

@app.route('/piping_estimator')
def get_cost():
    return flask.render_template("piping_estimator.html")

@app.route('/tools')
def show_tools():
    return flask.render_template("our_tools.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="8080", debug=True)
