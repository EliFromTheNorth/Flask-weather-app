from flask import Flask, render_template
from api import fetch_reather

app = Flask(__name__)

url = "https://api.open-meteo.com/v1/forecast?latitude=59.3294,55.6059,57.71,63.8284,67.8557&longitude=18.0687,13.0007,11.97,20.2597,20.2251&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&current=temperature_2m,wind_speed_10m&timezone=auto&forecast_days=3"

@app.route("/")
def index():
    return render_template("index.html")