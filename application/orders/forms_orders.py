from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, validators

class OrderFormNew(FlaskForm):
    address = StringField("Osoite", [validators.DataRequired(), validators.Length(min=5, max=32)])
    postal_code = IntegerField("Postinumero", [validators.DataRequired()])
    city = StringField("Kaupunki", [validators.DataRequired(), validators.Length(min=2, max=32)])
    button = SubmitField("Vahvista tilaus")

    class Meta:
        csrf = False