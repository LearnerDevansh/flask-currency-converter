from flask import Flask, render_template, request

app = Flask(__name__)

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
    result = error = None

    if request.method == "POST":
        try:
            amount = float(request.form["amount"])
            from_currency = request.form["from_currency"]
            to_currency = request.form["to_currency"]

            if from_currency == to_currency:
                converted_amount = amount
            elif from_currency in conversion_rates and to_currency in conversion_rates[from_currency]:
                rate = conversion_rates[from_currency][to_currency]
                converted_amount = amount * rate
            else:
                error = "Invalid conversion selection"
                return render_template("index.html", error=error)

            result = {
                "amount": amount,
                "from": from_currency,
                "to": to_currency,
                "converted_amount": round(converted_amount, 2)
            }

        except Exception as e:
            error = "Invalid input. Please enter a valid number."

    return render_template("index.html", result=result, error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
