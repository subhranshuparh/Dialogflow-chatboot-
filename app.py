from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "fca_live_ssonTjgHC3GeAoapedIhd93SzJuOcKSue3pswrjF"  # your key

@app.route('/', methods=['POST'])
def index():
    data = request.get_json()

    source_currency = data['queryResult']['parameters']['unit-currency']['currency']
    amount = data['queryResult']['parameters']['unit-currency']['amount']
    target_currency = data['queryResult']['parameters']['currency-name']

    print(f"{source_currency} {amount} {target_currency}")

    try:
        cf = convert(source_currency, target_currency)
        final_amount = amount * cf
        print(final_amount)

        response_text = f"{amount} {source_currency} = {final_amount:.2f} {target_currency}"

        return jsonify({
            "fulfillmentText": response_text
        })

    except Exception as e:
        print("Error:", e)
        return jsonify({
            "fulfillmentText": "Sorry, I couldn't fetch the conversion right now."
        })


def convert(source, target):
    url = f"https://api.freecurrencyapi.com/v1/latest?apikey={API_KEY}&base_currency={source}&currencies={target}"
    response = requests.get(url).json()
    
    return response["data"][target]


if __name__ == "__main__":
    app.run(debug=True)
