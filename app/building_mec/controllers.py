import flask

from app.building_mec import forms
#from bin import estimator

building_tools = flask.Blueprint('building_tools', __name__)


@building_tools.route('/building_tools/', defaults={"n": 2}, methods=["GET", "POST"])
@building_tools.route('/building_tools/<n>', methods=["GET", "POST"])
def building_description(n):
    form = forms.BetaHVACForm()
    for _ in range(n):
        form.add_entry()

    return flask.render_template("building_mec/building_description.html",
                                 title="Mécanique du bâtiment",
                                 form=form)
