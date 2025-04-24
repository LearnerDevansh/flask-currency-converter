from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect
from forms import CurrencyForm
from decimal import Decimal  # Import Decimal
import os

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "super-secret-key")
csrf = CSRFProtect(app)

conversion_rates = {
    "USD": {"INR": 83.0, "EUR": 0.93, "GBP": 0.80, "JPY": 151.5, "CAD": 1.36},
    "INR": {"USD": 1/83.0, "EUR": 0.0112, "GBP": 0.0096, "JPY": 1.83, "CAD": 0.0164},
    "EUR": {"USD": 1.08, "INR": 89.0, "GBP": 0.86, "JPY": 162.5, "CAD": 1.47},
    "GBP": {"USD": 1.25, "INR": 103.0, "EUR": 1.16, "JPY": 189.0, "CAD": 1.70},
    "JPY": {"USD": 0.0066, "INR": 0.55, "EUR": 0.0062, "GBP": 0.0053, "CAD": 0.009},
    "CAD": {"USD": 0.74, "INR": 61.0, "EUR": 0.68, "GBP": 0.59, "JPY": 111.0},
}

@app.route("/", methods=["GET", "POST"])
def index():
    form = CurrencyForm()
    result = error = None

    if form.validate_on_submit():
        try:
            # Convert form input to Decimal
            amount = Decimal(str(form.amount.data))  # ensures proper conversion
            from_currency = form.from_currency.data
            to_currency = form.to_currency.data

            if from_currency == to_currency:
                result = f"{amount:.2f} {from_currency} equals {amount:.2f} {to_currency}"
            else:
                rate = Decimal(str(conversion_rates[from_currency][to_currency]))  # Convert rate to Decimal
                converted = amount * rate
                result = f"{amount:.2f} {from_currency} equals {converted:.2f} {to_currency}"
        except Exception as e:
            error = f"Conversion error: {str(e)}"

    return render_template("index.html", form=form, result=result, error=error)

if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=5000, debug=debug_mode)
