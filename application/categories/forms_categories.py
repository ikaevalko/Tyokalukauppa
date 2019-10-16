from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, validators

class CategoryFormNew(FlaskForm):
    name = StringField("Kategorian nimi", [validators.Length(min=2, max=24)])
    button = SubmitField("Lisää kategoria")

    class Meta:
        csrf = False

class CategoryFormUpdate(FlaskForm):
    categories = SelectField("Päivitettävä kategoria", coerce=int)
    newName = StringField("Uusi nimi", [validators.Length(min=2, max=24)])
    button = SubmitField("Päivitä kategoria")

    class Meta:
        csrf = False

class CategoryFormDelete(FlaskForm):
    categories = SelectField("Valitse kategoria", coerce=int)
    button = SubmitField("Poista kategoria")

    class Meta:
        csrf = False