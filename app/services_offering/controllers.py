import flask
import json

from app import db

from app.services_offering import forms
from app.services_offering import Client

services_offering = flask.Blueprint('services_offering', __name__)


@services_offering.route('/', methods=["GET", "POST"])
def new_services_offer():
    if flask.request.method == "POST":
        form_data = flask.request.form

        flask.session['client'] = form_data['client']
        flask.session['mandate_type'] = form_data['mandate_type']
        flask.session['project_name'] = form_data['project_name']

        if flask.session['mandate_type'] == "Mécanique du bâtiment":
            url = 'services_offering.building_mechanic'
        else:
            url = 'services_offering.building_mechanic'

        return flask.redirect(flask.url_for(url))
    else:
        clients = Client.query.all()

        return flask.render_template('services_offering/ods.html',
                                     title="Offre de service",
                                     clients=clients,
                                     service_types=['Mécanique du bâtiment', 'Industriel', 'Énergétique'])


@services_offering.route('/building_mechanic', methods=["GET", "POST"])
def building_mechanic():
    if flask.request.method == "POST":
        form_data = flask.request.form
        flask.session['mec_inc'] = form_data.getlist("mec-inc")
        flask.session['mec_exc'] = form_data.getlist("mec-exc")
        flask.session['elec_inc'] = form_data.getlist("elec-inc")
        flask.session['elec_exc'] = form_data.getlist("elec-exc")

        return "Succes"
    else:
        if 'client' in flask.session:
            client = Client.query.filter_by(company_name=flask.session['client']).first()
            with open('bin/services_offering/project_specifications.json', 'r', encoding='utf-8') as json_file:
                defaults = json.load(json_file)
                default_specifications = defaults['building mechanics']
                default_mechanical_inclusions = defaults['building mechanics']['mechanical']['inclusions']
                default_mechanical_exclusions = defaults['building mechanics']['mechanical']['exclusions']
                default_electrical_inclusions = defaults['building mechanics']['electrical']['inclusions']
                default_electrical_exclusions = defaults['building mechanics']['electrical']['exclusions']
            return flask.render_template("services_offering/building_mechanic_form.html",
                                         client=client,
                                         default_specifications=default_specifications)
        else:
            msg = "Aucun client n'a été sélectionné. Veuillez sélectionner un client pour continuer."
            flask.flash(flask.Markup(msg), "info")
            return flask.render_template("services_offering/ods.html")



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