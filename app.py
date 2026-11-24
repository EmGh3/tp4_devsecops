import os
import sys
from flask import Flask, json, jsonify, request
import requests
import sys
import subprocess

app = Flask(__name__)

env = os.environ.copy()
env.setdefault(
    "SOPS_AGE_KEY_FILE",
    r"./age.key",
)


# Déchiffre secrets.enc.yaml au démarrage et charge les variables
proc = subprocess.run(
["sops", "--decrypt", "--input-type", "yaml", "--output-type", "json", "secrets.enc.yaml"],
    capture_output=True, text=True,env=env,
)

secrets = json.loads(proc.stdout)

WEATHER_API_KEY = secrets["WEATHER_API_KEY"]
AWS_ACCESS_KEY_ID = secrets["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = secrets["AWS_SECRET_ACCESS_KEY"]


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
