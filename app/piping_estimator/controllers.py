import flask

from app.piping_estimator import forms
from bin import estimator

tools = flask.Blueprint('piping_estimator', __name__)


@tools.route('/piping_beta/', defaults={"n": 2}, methods=["GET", "POST"])
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

            hourly_rate = form.salary_field.data
            bom_data = []
            item_time = 0
            item_cost = 0
            for r in range(0, n_rows):
                if form_data[r].quantity_field.data:
                    row_qty = form_data[r].quantity_field.data
                    if not row_qty in [float("inf"), float("-inf")]:
                        bom_data.append([r+1,
                                         form_data[r].item_field.data,
                                         form_data[r].diameter_field.data,
                                         form_data[r].schedule_field.data,
                                         form_data[r].material_field.data,
                                         form_data[r].quantity_field.data,
                                         item_time,
                                         item_cost])

            pipe_estimator = estimator.Estimator()
            total_time, total_cost, bom_data = pipe_estimator.man_hours(bom_data=bom_data, rate=hourly_rate)

            return flask.render_template("piping_estimator/piping_cost.html",
                                         title="Résultats",
                                         bom=bom_data,
                                         total_time=total_time,
                                         total_cost=total_cost,
                                         hourly_rate=hourly_rate)

        elif form.add_entry_field.data:
            form.add_entry()

        elif form.remove_entries_field.data:
            if not form.remove_entry():
                msg = "Il faut au minimum une ligne."
                flask.flash(msg, "info")

    return flask.render_template("piping_estimator/piping_beta.html",
                                 title="Estimateur Beta",
                                 form=form)
