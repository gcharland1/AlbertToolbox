import os
from app import app


if __name__ == '__main__':
    app.config['DIR'] = os.path.dirname(__file__)
    app.run(port='8080')