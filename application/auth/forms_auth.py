from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators

class LoginForm(FlaskForm):
    username = StringField("Käyttäjänimi")
    password = PasswordField("Salasana")
    button = SubmitField("Kirjaudu")

    class Meta:
        csrf = False

class RegisterForm(FlaskForm):
    name = StringField("Nimi", [validators.Length(min=2, max=144)])
    username = StringField("Käyttäjänimi", [validators.Length(min=2, max=64)])
    password = PasswordField("Salasana", [validators.Length(min=5, max=64)])
    button = SubmitField("Rekisteröidy")

    class Meta:
        csrf = False