from flask_wtf import FlaskForm
from wtforms import SelectField

class OrderByForm(FlaskForm):

    options = SelectField("Järjestä", choices=[("0", "Oletus"), ("1", "Halvimmat ensin"), ("2", "Kalleimmat ensin")])

    class Meta:
        csrf = False