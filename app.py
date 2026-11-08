from flask import Flask, render_template, request, redirect, url_for
from api import fetch_weather
import logging
from weather_service import weather_dashboard, cities, city_name_list, units

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
# app.jinja_env.filters['units'] = units

url = "https://api.open-meteo.com/v1/forecast?latitude=59.3294,55.6059,57.71,63.8284,67.8557&longitude=18.0687,13.0007,11.97,20.2597,20.2251&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&current=temperature_2m,wind_speed_10m&timezone=auto&forecast_days=3"

@app.errorhandler(404)
def error404(error):
    return render_template("error404.html"), 404

@app.route("/")
def index():
    selected_city = request.args.get("selected_city")
    if selected_city:
        return redirect(url_for('weather', city_name=selected_city))
    city_names = city_name_list()
    return render_template("index.html", cities=city_names)

@app.route("/<city_name>")
def weather(city_name):
    html_current, html_3days = weather_dashboard(city_name)
    return render_template("city_name.html", city=city_name, dashboard=html_3days, current_weather = html_current)
