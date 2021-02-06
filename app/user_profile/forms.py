from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class EditProfileFrom(FlaskForm):
    username = StringField('Nom d''utilisateur', validators=[Length(min=2, max=20)])
    email = StringField('Email', validators=[Email()])
    old_password = PasswordField('Mot de passe actuel', validators=[DataRequired()])
    new_password = PasswordField('Nouveau mot de passe',
                                 validators=[EqualTo('confirm_new_password')])
    confirm_new_password = PasswordField('Confirmer nouveau mot de passe',
                                         validators=[EqualTo('new_password')])
    submit = SubmitField('Enregistrer')
