from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, SelectField, FieldList, FormField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('Nom d''utilisateur', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmer mot de passe', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Créer mon compte')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    submit = SubmitField('Se connecter')

class PipingForm(FlaskForm):
    file = FileField('Fichier image', validators=[DataRequired()])
    submit = SubmitField('Calculer les coûts')

class BetaPipingItemForm(FlaskForm):
    item_list = ["Coude", "Valve", "Bride", "Tuyau"]
    diameter_list = ["1", "1-1/2", "2", "2-1/2", "3", "4", "6", "8", "10", "12", "14", "16"]
    schedule_list = ["10", "20", "40", "80"]
    material_list = ["Acier Carbone", "Innox"]

    item_field = SelectField("Type d'élément", choices=item_list, validators=[DataRequired()])
    diameter_field = SelectField("Diamètre (po)", choices=diameter_list, validators=[DataRequired()])
    schedule_field = SelectField("Schedule", choices=schedule_list, validators=[DataRequired()])
    material_field = SelectField("Matériel", choices=material_list, validators=[DataRequired()])
    quantity_field = StringField("Quantité/Longueur (pi)", validators=[DataRequired()])

class BetaPipingForm(FlaskForm):
    rows = FieldList(FormField(BetaPipingItemForm))
    n_rows = 0
    submit_field = SubmitField("Calculer les coûts")
