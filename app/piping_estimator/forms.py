from app import app
from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField, SelectField, FieldList, FormField, BooleanField, FloatField
from wtforms.validators import DataRequired
import json
import os


class PipingForm(FlaskForm):
    file = FileField('Fichier image', validators=[DataRequired()])
    submit = SubmitField('Calculer les coûts')


class BetaPipingItemForm(FlaskForm):
    with open(os.path.join(app.config['BASE_DIR'], 'bin/dictionaries/operation_times.json'), 'r') as json_file:
        op_data = json.load(json_file)
        item_list = op_data['Count'].keys()
        diameter_list = op_data['Time']['Weld'].keys()
        schedule_list = op_data['Schedule Factors'].keys()
        material_list = op_data['Material Factors'].keys()

    select_field = BooleanField("Sélectionner")
    item_field = SelectField("Type d'élément", choices=item_list, validators=[DataRequired()])
    diameter_field = SelectField("Diamètre (po)", choices=diameter_list, default=4, validators=[DataRequired()])
    schedule_field = SelectField("Schedule", choices=schedule_list, default=40, validators=[DataRequired()])
    material_field = SelectField("Matériel", choices=material_list, validators=[DataRequired()])
    quantity_field = FloatField("Quantité/Longueur (pi)", default=0, validators=[DataRequired()])


class BetaPipingForm(FlaskForm):
    n_rows = 0

    rows = FieldList(FormField(BetaPipingItemForm))
    salary_field = FloatField("Taux horaire ($/hr)", default=100, validators=[DataRequired()])
    add_entry_field = SubmitField("Ajouter une ligne")
    remove_entries_field = SubmitField("Retirer une ligne")
    submit_field = SubmitField("Calculer le temps de fabrication")

    def add_entry(self, copy=False):
        self.rows.append_entry()
        self.n_rows += 1
        if copy and self.n_rows > 1:
            self.rows[self.n_rows-1].diameter_field.data = self.rows[self.n_rows-2].diameter_field.data
            self.rows[self.n_rows-1].schedule_field.data = self.rows[self.n_rows-2].schedule_field.data
            self.rows[self.n_rows-1].material_field.data = self.rows[self.n_rows-2].material_field.data

    def remove_entry(self):
        if self.n_rows > 1:
            self.rows.pop_entry()
            self.n_rows -= 1
            return True
        else:
            return False
