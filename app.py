from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Really amazing app mate!'


@app.route('/get_cost')
def get_cost():
    return 'This piping will be very expensive my guy!'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="8080")
