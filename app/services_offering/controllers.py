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

        flask.session['offer'] = {}
        flask.session['offer']['client_company'] = form_data['client']
        flask.session['offer']['mandate_type'] = form_data['mandate_type']
        flask.session['offer']['project_name'] = form_data['project_name']

        if flask.session['offer']['mandate_type'] == "Mécanique du bâtiment":
            url = 'services_offering.building_mechanic'
            url = 'services_offering.define_mandate'
        else:
            url = 'services_offering.define_mandate'

        return flask.redirect(flask.url_for(url))
    else:
        clients = Client.query.all()
        offer_types = ['Mécanique du bâtiment', 'Industriel', 'Énergétique', 'Autre']
        available_forms = ['Mécanique du bâtiment', 'Autre']
        return flask.render_template('services_offering/ods.html',
                                     title="Offre de service",
                                     clients=clients,
                                     service_types=offer_types,
                                     available_forms=available_forms)

@services_offering.route('/define_mandate', methods=["GET", "POST"])
def define_mandate():
    if 'client_company' in flask.session['offer']:
        client = Client.query.filter_by(company_name=flask.session['offer']['client_company']).first()
    else:
        msg = "Aucun client n'a été sélectionné. Veuillez sélectionner un client pour continuer."
        flask.flash(flask.Markup(msg), "info")
        return flask.redirect(flask.url_for('services_offering.new_services_offer'))

    if flask.request.method == "POST":
        form_data = flask.request.form

        flask.session['offer']['mandate'] = form_data['role']
        flask.session['offer']['mandate_details'] = {}

        details_categories = form_data.getlist('details-category')
        for cat in details_categories:
            flask.session['offer']['mandate_details'][cat] = form_data.getlist(cat)
            print(cat, form_data.getlist(cat))

        flask.session['offer']['inclusions_defined'] = True
        flask.session.modified = True

        url = "services_offering.price_definition"

        return flask.redirect(flask.url_for(url))
    else:
        if not 'mandate_defined' in flask.session['offer']:
            mandate_type = flask.session['offer']['mandate_type']

            with open(os.path.join(app.config['BASE_DIR'], 'bin/services_offering/project_specifications.json'),
                      'r', encoding='utf-8') as json_file:
                defaults = json.load(json_file)

                if mandate_type in defaults.keys():
                    flask.session['offer']['mandate_details'] = {}
                    for cat in defaults[mandate_type].keys():
                        flask.session['offer']['mandate_details'][cat] = defaults[mandate_type][cat]

        return flask.render_template('services_offering/define_mandate.html',
                                     title='Détails du mandat',
                                     client = client)

@services_offering.route('/building_mechanic', methods=["GET", "POST"])
def building_mechanic():
    if 'client_company' in flask.session['offer']:
        client = Client.query.filter_by(company_name=flask.session['offer']['client_company']).first()
    else:
        msg = "Aucun client n'a été sélectionné. Veuillez sélectionner un client pour continuer."
        flask.flash(flask.Markup(msg), "info")
        return flask.redirect(flask.url_for('services_offering.new_services_offer'))
    if flask.request.method == "POST":

        form_data = flask.request.form

        flask.session['offer']['mandate'] = form_data['role']

        flask.session['offer']['mec_inc'] = form_data.getlist("mec-inc")
        flask.session['offer']['mec_exc'] = form_data.getlist("mec-exc")
        flask.session['offer']['elec_inc'] = form_data.getlist("elec-inc")
        flask.session['offer']['elec_exc'] = form_data.getlist("elec-exc")

        flask.session['offer']['inclusions_defined'] = True

        flask.session.modified = True

        url = "services_offering.price_definition"

        return flask.redirect(flask.url_for(url))


    else:
        if not 'inclusions_defined' in flask.session['offer']:
            print('Defining inclusions')
            with open(os.path.join(app.config['BASE_DIR'], 'bin/services_offering/project_specifications.json'), 'r', encoding='utf-8') as json_file:
                defaults = json.load(json_file)
                flask.session['offer']['mec_inc'] = defaults['building mechanics']['mechanical']['inclusions']
                flask.session['offer']['mec_exc'] = defaults['building mechanics']['mechanical']['exclusions']
                flask.session['offer']['elec_inc'] = defaults['building mechanics']['electrical']['inclusions']
                flask.session['offer']['elec_exc'] = defaults['building mechanics']['electrical']['exclusions']
                flask.session.modified = True

        return flask.render_template("services_offering/building_mechanic_form.html",
                                     title="Offre de services",
                                     client=client)

@services_offering.route('/pricing', methods=["GET", "POST"])
def price_definition():
    if 'client_company' in flask.session['offer']:
        client = Client.query.filter_by(company_name=flask.session['offer']['client_company']).first()
    else:
        msg = "Aucun client n'a été sélectionné. Veuillez sélectionner un client pour commencer."
        flask.flash(flask.Markup(msg), "info")
        return flask.redirect(flask.url_for('services_offering.new_services_offer'))

    if flask.request.method == "POST":
        form_data = flask.request.form

        flask.session['offer']['price_descriptions'] = form_data.getlist('price-description')
        flask.session['offer']['prices'] = form_data.getlist('price', type=int)
        flask.session['offer']['total_price'] = sum(flask.session['offer']['prices'])
        flask.session['offer']['prices_defined'] = True

        flask.session.modified = True

        return flask.redirect(flask.url_for('services_offering.review_offer'))
    else:
        return flask.render_template('services_offering/project_rate.html',
                                     title='Honoraires',
                                     client=client)

@services_offering.route('/review')
def review_offer():
    if 'client_company' in flask.session['offer']:
        client = Client.query.filter_by(company_name=flask.session['offer']['client_company']).first()

        return flask.render_template('services_offering/review_offer.html',
                                     title="Offre de services",
                                     client=client)
    else:
        msg = "Aucun client n'a été sélectionné. Veuillez sélectionner un client pour continuer."
        flask.flash(flask.Markup(msg), "info")
        return flask.redirect(flask.url_for('services_offering.new_services_offer'))

@services_offering.route('/generate_pdf')
def generate_pdf():
    if flask.session['offer']['mandate_type'] == 'Mécanique du bâtiment':
        useful_keys = ['project_name',
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
        useful_keys = []

    client = Client.query.filter_by(company_name=flask.session['offer']['client_company']).first()

    data = {}
    data['contact_fname'] = client.contact_fname
    data['contact_name'] = client.contact_name
    data['client_company'] = client.company_name
    data['client_address'] = client.address
    data['client_city'] = client.city
    data['client_province'] = client.province
    data['client_zip'] = client.zip

    for key in flask.session['offer']:
        if key in useful_keys:
            data[key] = flask.session['offer'][key]

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

