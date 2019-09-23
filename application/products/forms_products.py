from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DecimalField, IntegerField, SubmitField, validators

class ProductFormNew(FlaskForm):
    name = StringField("Tuotteen nimi", [validators.Length(min=2, max=64)])
    desc = TextAreaField("Tuotteen kuvaus", [validators.Length(min=0, max=128)])
    price = DecimalField("Hinta", [validators.NumberRange(min=0, max=9999)])
    quantity = IntegerField("Saldo", [validators.NumberRange(min=0, max=9999)])

    class Meta:
        csrf = False