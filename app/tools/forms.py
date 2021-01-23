from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, SelectField, FieldList, FormField, BooleanField
from wtforms.validators import DataRequired
import json


class PipingForm(FlaskForm):
    file = FileField('Fichier image', validators=[DataRequired()])
    submit = SubmitField('Calculer les coûts')

class BetaPipingItemForm(FlaskForm):
    with open('bin/dictionaries/operation_times.json', 'r') as json_file:
        op_data = json.load(json_file)
        item_list = op_data['Count'].keys()
        diameter_list = op_data['Time']['Weld'].keys()
        schedule_list = op_data['Sch Factors'].keys()
        material_list = op_data['Mtl Factors'].keys()

    select_field = BooleanField("Sélectionner")
    item_field = SelectField("Type d'élément", choices=item_list, validators=[DataRequired()])
    diameter_field = SelectField("Diamètre (po)", choices=diameter_list, validators=[DataRequired()])
    schedule_field = SelectField("Schedule", choices=schedule_list, validators=[DataRequired()])
    material_field = SelectField("Matériel", choices=material_list, validators=[DataRequired()])
    quantity_field = StringField("Quantité/Longueur (pi)", validators=[DataRequired()])

class BetaPipingForm(FlaskForm):
    rows = FieldList(FormField(BetaPipingItemForm))
    n_rows = 0
    submit_field = SubmitField("Calculer les coûts")
