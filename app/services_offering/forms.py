from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField, SelectField, FieldList, FormField, BooleanField, FloatField, StringField
from wtforms.validators import DataRequired


class ClientForm(FlaskForm):
    last_name = StringField('Nom', validators=[DataRequired()])
    first_name = StringField('Prénom', validators=[DataRequired()])
    company = StringField('Compagnie', validators=[DataRequired()])
    address = StringField('Adresse', validators=[DataRequired()])
    city = StringField('Ville', default="Sherbrooke", validators=[DataRequired()])
    province = StringField('Province', default="Qc", validators=[DataRequired()])
    zip = StringField('Code Postal', validators=[DataRequired()])

class ProjectDetail(FlaskForm):
    n = 0
    list = FormField(StringField)
    add_button = SubmitField('Ajouter un élément')
    rem_button = SubmitField('Retirer un élément')

    def add_item(self):
        self.n += 1
        self.list.add_entry()

    def rem_item(self):
        if self.n > 0:
            self.n -= 1
            self.list.pop_entry()

class ProjectForm(FlaskForm):
    mandate = StringField('Description du mandat', validators=[DataRequired()])

    mechanical_inclusions = FormField(ProjectDetail, label="Inclusions mécaniques")
    mechanical_exclusions = FormField(ProjectDetail, label="Exclusions mécaniques")
    electrical_inclusions = FormField(ProjectDetail, label="Inclusions électriques")
    electrical_exclusions = FormField(ProjectDetail, label="Exclusions électriques")

class ServicesForm(FlaskForm):
    client_description = FormField(ClientForm, label="Client")
    project_description = FormField(ProjectForm, label="Projet")
    submit = SubmitField("Générer l'offre de services")