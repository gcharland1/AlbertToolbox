import flask

from app.tools import forms
from bin import estimator

tools = flask.Blueprint('tools', __name__)


@tools.route('/piping_beta/', defaults={"n": 5}, methods=["GET", "POST"])
@tools.route('/piping_beta/<n>', methods=["GET", "POST"])
def piping_beta(n):
    n = int(n)
    form = forms.BetaPipingForm()
    for _ in range(n):
        form.add_entry()

    if flask.request.method == "POST":
        if form.submit_field.data:
            form_data = form.rows
            n_rows = len(form_data)

            bom_data = []
            for r in range(n_rows):
                if not (form_data[r].quantity_field.data == None):
                    if form_data[r].quantity_field.data > 0:
                        bom_data.append([r+1,
                                         form_data[r].item_field.data,
                                         form_data[r].diameter_field.data,
                                         form_data[r].schedule_field.data,
                                         form_data[r].material_field.data,
                                         form_data[r].quantity_field.data,
                                         0])

            pipe_estimator = estimator.Estimator()
            total_time, bom_data = pipe_estimator.man_hours(bom_data)

            return flask.render_template("tools/piping_cost.html",
                                         title="Résultats",
                                         bom=bom_data,
                                         total_time=total_time)

        elif form.add_entry_field.data:
            form.add_entry()

        elif form.remove_entries_field.data:
            form.remove_entry()

    return flask.render_template("tools/piping_beta.html",
                                 title="Estimateur Beta",
                                 form=form)

@tools.route('/tools', methods=["GET", "POST"])
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
        return flask.render_template("tools/tools.html", title="Estimateur de coûts", form=form)