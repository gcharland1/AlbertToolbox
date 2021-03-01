import flask

from app.services_offering import forms

services_offering = flask.Blueprint('services_offering', __name__)


@services_offering.route('/ods/', methods=["GET", "POST"])
def services_offer():
    form = forms.ServicesForm()

    if flask.request.method == "POST":
        return "POST"
    else:
        return flask.render_template('services_offering/ods.html',
                                     title="Offre de service",
                                     form=form)

