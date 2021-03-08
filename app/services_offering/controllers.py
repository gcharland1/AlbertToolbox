import flask
import json
import os

from app import db
from app import app

from app.services_offering import Client
from bin.services_offering.generate_latex_report import ReportBuilder

services_offering = flask.Blueprint('services_offering', __name__)


@services_offering.route('/', methods=["GET", "POST"])
def new_services_offer():
    if flask.request.method == "POST":
        form_data = flask.request.form

        flask.session['client_company'] = form_data['client']
        flask.session['mandate_type'] = form_data['mandate_type']
        flask.session['project_name'] = form_data['project_name']

        if flask.session['mandate_type'] == "Mécanique du bâtiment":
            url = 'services_offering.building_mechanic'
        else:
            url = 'services_offering.building_mechanic'

        return flask.redirect(flask.url_for(url))
    else:
        indices = ['client_company', 'price_defined', 'inclusions_defined']
        clear_session(indices)
        clients = Client.query.all()
        return flask.render_template('services_offering/ods.html',
                                     title="Offre de service",
                                     clients=clients,
                                     service_types=['Mécanique du bâtiment', 'Industriel', 'Énergétique'])

@services_offering.route('/building_mechanic', methods=["GET", "POST"])
def building_mechanic():
    if 'client_company' in flask.session:
        client = Client.query.filter_by(company_name=flask.session['client_company']).first()

        if flask.request.method == "POST":
            form_data = flask.request.form
            flask.session['mandate'] = form_data['role']

            flask.session['mec_inc'] = form_data.getlist("mec-inc")
            flask.session['mec_exc'] = form_data.getlist("mec-exc")
            flask.session['elec_inc'] = form_data.getlist("elec-inc")
            flask.session['elec_exc'] = form_data.getlist("elec-exc")

            flask.session['inclusions_defined'] = True

            return flask.redirect(flask.url_for('services_offering.price_definition'))

        else:
            if not 'inclusions_defined' in flask.session:
                with open(os.path.join(app.config['BASE_DIR'], 'bin/services_offering/project_specifications.json'), 'r', encoding='utf-8') as json_file:
                    defaults = json.load(json_file)
                    flask.session['mec_inc'] = defaults['building mechanics']['mechanical']['inclusions']
                    flask.session['mec_exc'] = defaults['building mechanics']['mechanical']['exclusions']
                    flask.session['elec_inc'] = defaults['building mechanics']['electrical']['inclusions']
                    flask.session['elec_exc'] = defaults['building mechanics']['electrical']['exclusions']

            return flask.render_template("services_offering/building_mechanic_form.html",
                                         title="Offre de services",
                                         client=client)
    else:
        msg = "Aucun client n'a été sélectionné. Veuillez sélectionner un client pour continuer."
        flask.flash(flask.Markup(msg), "info")
        return flask.redirect(flask.url_for('services_offering.new_services_offer'))

@services_offering.route('/pricing', methods=["GET", "POST"])
def price_definition():
    if 'client_company' in flask.session:
        client = Client.query.filter_by(company_name=flask.session['client_company']).first()

        if flask.request.method == "POST":
            form_data = flask.request.form
            flask.session['price_descriptions'] = form_data.getlist('price-description')
            flask.session['prices'] = form_data.getlist('price', type=int)

            flask.session['total_price'] = sum(flask.session['prices'])

            flask.session['prices_defined'] = True

            return flask.redirect(flask.url_for('services_offering.review_offer'))
        else:
            return flask.render_template('services_offering/project_rate.html',
                                         title='Offre de service',
                                         client=client)
    else:
        msg = "Aucun client n'a été sélectionné. Veuillez sélectionner un client pour continuer."
        flask.flash(flask.Markup(msg), "info")
        return flask.redirect(flask.url_for('services_offering.new_services_offer'))

@services_offering.route('/review', methods=["POST", "GET"])
def review_offer():
    if 'client_company' in flask.session:
        client = Client.query.filter_by(company_name=flask.session['client_company']).first()

        if flask.request.method == "POST":
            return "POST"
        else:
            return flask.render_template('services_offering/review_offer.html',
                                         title="Offre de services",
                                         client=client)
    else:
        msg = "Aucun client n'a été sélectionné. Veuillez sélectionner un client pour continuer."
        flask.flash(flask.Markup(msg), "info")
        return flask.redirect(flask.url_for('services_offering.new_services_offer'))

@services_offering.route('/generate_pdf')
def generate_pdf():
    if flask.session['mandate_type'] == 'Mécanique du bâtiment':
        useful_indices = ['project_name',
                           'mandate',
                           'mec_inc',
                           'mec_exc',
                           'elec_inc',
                           'elec_exc',
                           'prices',
                           'price_descriptions',
                           'total_price',
                           'client']
    else:
        useful_indices = []

    client = Client.query.filter_by(company_name=flask.session['client_company']).first()

    data = {}
    data['contact_fname'] = client.contact_fname
    data['contact_name'] = client.contact_name
    data['client_company'] = client.company_name
    data['client_address'] = client.address
    data['client_city'] = client.city
    data['client_province'] = client.province
    data['client_zip'] = client.zip

    for index in flask.session:
        if index in useful_indices:
            data[index] = flask.session[index]

    report_builder = ReportBuilder()
    work_dir = os.path.join(app.config['BASE_DIR'], 'bin/services_offering/latex/')
    pdf_file = report_builder.building_mechanics(work_dir, data)

    return flask.send_from_directory(work_dir, pdf_file)

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

def clear_session(keys):
    for i in keys:
        if i in flask.session:
            flask.session.pop(i)