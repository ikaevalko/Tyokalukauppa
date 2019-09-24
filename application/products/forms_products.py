from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DecimalField, IntegerField, SubmitField, validators

class ProductFormNew(FlaskForm):
    name = StringField("Tuotteen nimi", [validators.Length(min=2, max=64)])
    desc = TextAreaField("Tuotteen kuvaus", [validators.Length(min=0, max=255)])
    price = DecimalField("Hinta", [validators.NumberRange(min=0, max=9999)])
    quantity = IntegerField("Saldo", [validators.NumberRange(min=0, max=9999)])
    category = StringField("Kategoria")
    button = SubmitField("Lisää tuote")

    class Meta:
        csrf = False

class ProductFormUpdate(FlaskForm):
    name = StringField("Tuotteen nimi", [validators.Length(min=2, max=64)])
    desc = TextAreaField("Tuotteen kuvaus", [validators.Length(min=0, max=255)])
    price = DecimalField("Hinta", [validators.NumberRange(min=0, max=9999)])
    quantity = IntegerField("Saldo", [validators.NumberRange(min=0, max=9999)])
    category = StringField("Kategoria")
    button = SubmitField("Lisää tuote")

    class Meta:
        csrf = False

class ProductFormDelete(FlaskForm):
    name = StringField("Tuotteen nimi")
    button = SubmitField("Poista tuote")

    class Meta:
        csrf = False