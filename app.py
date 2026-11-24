from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# VULNÉRABILITÉ VOLONTAIRE : secret codé en dur (fausses valeurs)
WEATHER_API_KEY = "sk_live_51Nf8Xk2eZvKYlo9aQ7mTz3PdR4uW6bHc"
AWS_ACCESS_KEY_ID = "AKIAJ3KQ7VZ5TPLM2XNB"
AWS_SECRET_ACCESS_KEY = "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"


@app.route("/health")
def health():
    return jsonify(status="ok")


@app.route("/weather")
def weather():
    city = request.args.get("city", "Tunis")
    r = requests.get(
        "https://api.example-weather.com/v1/current",
        params={"q": city, "key": WEATHER_API_KEY},
        timeout=5,
    )
    return jsonify(r.json()), r.status_code


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
