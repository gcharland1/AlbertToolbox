import flask

from app.tools import forms

tools = flask.Blueprint('tools', __name__, )

@tools.route('/piping_estimator', methods=["GET", "POST"])
def piping_estimator():
    if "premium" in flask.session:
        form = forms.PipingForm()
        if flask.request.method == 'POST':
            filename = form.file.data.filename
            print(filename)
            file_data = flask.request.files[form.file.name].read()
            image_path = os.path.join(app.config["UPLOAD_PATH"], filename)
            open(image_path, 'wb').write(file_data)
            reader = image_reader.ImageReader()
            bom_content = reader.image_to_text_table(image_path)
            os.remove(image_path)
            return flask.url_for("name", name=bom_content)

        else:
            return flask.render_template("tools/piping_estimator.html", title="Estimateur de coûts", form=form)
    else:
        form = forms.BetaPipingForm()
        if flask.request.method == "POST":
            return "Success"
        else:
            for i in range(5):
                form.rows.append_entry()
                form.n_rows += 1

        return flask.render_template("tools/piping_beta.html", title="Estimateur Beta", form=form)
