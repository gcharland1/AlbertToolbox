import flask

from app import db

from app.services_offering import forms
from app.services_offering import Client

services_offering = flask.Blueprint('services_offering', __name__)


@services_offering.route('/ods', methods=["GET", "POST"])
def new_services_offer():

    if flask.request.method == "POST":
        return "POST"
    else:
        clients = Client.query.all()

        return flask.render_template('services_offering/ods.html',
                                     title="Offre de service",
                                     clients=clients,
                                     service_types=['Mécanique du bâtiment', 'Industriel', 'Énergétique'])


@services_offering.route('/new_client', methods=["GET", "POST"])
def new_client():
    if flask.request.method == "POST":
        form_data = flask.request.form

        fname = form_data["fname"]
        name = form_data["name"]
        company = form_data["company"]
        address = form_data["address"]
        city = form_data["city"]
        province = form_data["province"]
        zip = form_data["zip"]

        client = Client(fname, name, company, address, city, province, zip)
        db.session.add(client)
        db.session.commit()

        return flask.redirect(flask.url_for('services_offering.new_services_offer'))

    return flask.render_template('services_offering/new_client.html')