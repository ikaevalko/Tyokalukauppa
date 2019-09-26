from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DecimalField, IntegerField, SubmitField, HiddenField, validators

class ProductFormNew(FlaskForm):
    name = StringField("Tuotteen nimi", [validators.Length(min=2, max=64)])
    desc = TextAreaField("Tuotteen kuvaus", [validators.Length(min=0, max=400)])
    price = DecimalField("Hinta", [validators.NumberRange(min=0, max=9999)])
    quantity = IntegerField("Saldo", [validators.NumberRange(min=0, max=9999)])
    category = StringField("Kategoria")
    button = SubmitField("Lisää tuote")

    class Meta:
        csrf = False

class ProductFormUpdate(FlaskForm):
    oldName = StringField("Päivitettävä tuote")
    hiddenName = HiddenField("H")
    button_get = SubmitField("Hae tuote")

    name = StringField("Tuotteen nimi", [validators.Length(min=2, max=64)])
    desc = TextAreaField("Tuotteen kuvaus", [validators.Length(min=0, max=400)])
    price = DecimalField("Hinta", [validators.NumberRange(min=0, max=9999)])
    quantity = IntegerField("Saldo", [validators.NumberRange(min=0, max=9999)])
    category = StringField("Kategoria")
    button_update = SubmitField("Päivitä tuote")

    class Meta:
        csrf = False

class ProductFormDelete(FlaskForm):
    name = StringField("Tuotteen nimi")
    button = SubmitField("Poista tuote")

    class Meta:
        csrf = False