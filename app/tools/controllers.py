import flask

from app import db
from app.tools import forms
from bin import estimator

tools = flask.Blueprint('tools', __name__, )

@tools.route('/piping_beta', methods=["GET", "POST"])
def piping_beta(n_rows=10):
    form = forms.BetaPipingForm()
    if flask.request.method == "POST":
        form_rows = form.rows
        bom_rows = []
        for r in form_rows:
            bom_rows.append([r.item_field.data,
                             r.diameter_field.data,
                             r.schedule_field.data,
                             r.material_field.data,
                             r.quantity_field.data])
        return str(bom_rows)
    else:
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