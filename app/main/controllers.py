import flask
import os

from app import ColorScheme

main = flask.Blueprint('main', __name__, )


@main.route('/')
def home():
    content_dir = "app/static/content/index"
    titles, contents = get_content(content_dir)

    return flask.render_template("index.html", title="Accueil", titles=titles, content=contents)

@main.route('/tools')
def show_tools():
    content_dir = "app/static/content/our_tools"
    titles, contents = get_content(content_dir)

    return flask.render_template("index.html", title="Nos Outils", titles=titles, content=contents)

def get_content(dir):
    titles = []
    contents = []

    files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]

    for file in files:
        print(file)
        file_title, file_content = read_article(os.path.join(dir, file))
        contents.append(file_content)
        titles.append(file_title)

    return titles, contents

def read_article(file):
    line_count = 0
    title = ""
    content = []
    with open(file, 'r', encoding='utf-8') as f:
        content_line = ""
        for r in f:
            if line_count == 0:
                title += r
                line_count += 1
            else:
                if r == "\n":
                    content.append(content_line)
                    content_line = ""
                else:
                    content_line += r
        content.append(content_line)

    return title, content

