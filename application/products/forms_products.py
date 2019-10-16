from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DecimalField, IntegerField, SubmitField, SelectField, validators

class ProductFormNew(FlaskForm):
    name = StringField("Tuotteen nimi", [validators.Length(min=2, max=64)])
    description = TextAreaField("Tuotteen kuvaus", [validators.Length(min=0, max=400)])
    price = DecimalField("Hinta", [validators.NumberRange(min=0, max=9999)])
    quantity = IntegerField("Saldo", [validators.NumberRange(min=0, max=9999)])
    category = SelectField("Kategoria", coerce=int)
    button = SubmitField("Lisää tuote")

    class Meta:
        csrf = False

class ProductFormUpdate(FlaskForm):
    name = StringField("Tuotteen nimi", [validators.Length(min=2, max=64)])
    description = TextAreaField("Tuotteen kuvaus", [validators.Length(min=0, max=400)])
    price = DecimalField("Hinta", [validators.NumberRange(min=0, max=9999)])
    quantity = IntegerField("Saldo", [validators.NumberRange(min=0, max=9999)])
    category = SelectField("Kategoria", coerce=int)
    button = SubmitField("Päivitä tuote")

    class Meta:
        csrf = False