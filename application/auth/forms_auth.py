from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators

class LoginForm(FlaskForm):
    username = StringField("Käyttäjänimi", [validators.DataRequired()])
    password = PasswordField("Salasana", [validators.DataRequired()])
    button = SubmitField("Kirjaudu")

    class Meta:
        csrf = False

class RegisterForm(FlaskForm):
    name = StringField("Nimi", [validators.DataRequired(), validators.Length(min=2, max=32)])
    username = StringField("Käyttäjänimi", [validators.DataRequired(), validators.Length(min=2, max=32)])
    password = PasswordField("Salasana", [validators.DataRequired(), validators.Length(min=5, max=32)])
    button = SubmitField("Rekisteröidy")

    class Meta:
        csrf = False