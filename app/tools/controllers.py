import flask

from app import db
from app.tools import forms
from bin import estimator

tools = flask.Blueprint('tools', __name__, )

@tools.route('/piping_beta', methods=["GET", "POST"])
def piping_beta():
    form = forms.BetaPipingForm()
    if flask.request.method == "POST":
        form_rows = form.rows
        n_rows = len(form.rows)

        bom_rows = []
        for r in range(n_rows):
            bom_rows.append([r+1,
                             form_rows[r].item_field.data,
                             form_rows[r].diameter_field.data,
                             form_rows[r].schedule_field.data,
                             form_rows[r].material_field.data,
                             form_rows[r].quantity_field.data,
                             0])

        pipe_estimator = estimator.Estimator()
        total_time, bom_rows = pipe_estimator.man_hours(bom_rows)

        return str(total_time)
    else:
        n_rows = 3
        for i in range(n_rows):
            form.rows.append_entry()
            form.n_rows += 1

    return flask.render_template("tools/piping_beta.html", title="Estimateur Beta", form=form, n_rows=n_rows)

@tools.route('/piping_estimator', methods=["GET", "POST"])
def piping_estimator():
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