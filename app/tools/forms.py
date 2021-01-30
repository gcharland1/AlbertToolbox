from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField, SelectField, FieldList, FormField, BooleanField, FloatField
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
    quantity_field = FloatField("Quantité/Longueur (pi)", default=0, validators=[DataRequired()])

class BetaPipingForm(FlaskForm):
    n_rows = 0

    rows = FieldList(FormField(BetaPipingItemForm))

    add_entry_field = SubmitField("Ajouter une ligne")
    remove_entries_field = SubmitField("Retirer une ligne")
    submit_field = SubmitField("Calculer les coûts")

    def add_entry(self):
        self.rows.append_entry()
        self.n_rows += 1

    def remove_entry(self):
        if self.n_rows > 1:
            self.rows.pop_entry()
            self.n_rows -= 1
            return True
        else:
            return False