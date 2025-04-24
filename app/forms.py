from flask_wtf import FlaskForm
from wtforms import DecimalField, SelectField, SubmitField
from wtforms.validators import DataRequired

class CurrencyForm(FlaskForm):
    amount = DecimalField('Amount', validators=[DataRequired()])
    from_currency = SelectField('From', choices=[('USD','USD'), ('INR','INR'), ('EUR','EUR'), ('GBP','GBP'), ('JPY','JPY'), ('CAD','CAD')])
    to_currency = SelectField('To', choices=[('INR','INR'), ('USD','USD'), ('EUR','EUR'), ('GBP','GBP'), ('JPY','JPY'), ('CAD','CAD')])
    submit = SubmitField('Convert')
