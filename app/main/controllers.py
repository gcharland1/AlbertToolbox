import flask
import os
import markdown as md

from app import app

main = flask.Blueprint('main', __name__, )

@main.route('/')
def home():
    content_dir = "app/static/content/index"
    abs_dir = os.path.join(app.config['BASE_DIR'], content_dir)
    titles, contents = get_content(abs_dir)

    return flask.render_template("main/content_page.html", title="Accueil", titles=titles, content=contents)

@main.route('/piping_estimator')
def show_tools():
    content_dir = "app/static/content/our_tools"
    abs_dir = os.path.join(app.config['BASE_DIR'], content_dir)
    titles, contents = get_content(abs_dir)

    return flask.render_template("main/content_page.html", title="Nos Outils", titles=titles, content=contents)

def get_content(dir):
    titles = []
    contents = []

    files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]

    for file in files:
        file_title, file_content = read_article(os.path.join(dir, file))
        contents.append(file_content)
        titles.append(file_title)

    return titles, contents

def read_article(file):
    line_count = 0
    title = ""
    content = ""
    with open(file, 'r', encoding='utf-8') as f:
        for r in f:
            if line_count == 0:
                title += r
                line_count += 1
            else:
                content += r

    md_title = md.markdown(title)
    md_content = md.markdown(content)
    return md_title, md_content

