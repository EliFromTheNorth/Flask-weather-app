from flask import Flask, render_template, request, redirect, url_for
from api import fetch_weather
import logging
from weather_service import weather_dashboard, cities, city_name_list

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
# app.jinja_env.filters['units'] = units

@app.errorhandler(404)
def error404(error):
    return render_template("error404.html"), 404

@app.route("/")
def index():
    selected_city = request.args.get("selected_city")
    if selected_city:
        return redirect(url_for('weather', city_name=selected_city))
    try:
        city_names = city_name_list()
    except RuntimeError as e:
        return render_template("index.html", cities=[], error=str(e)), 502
    return render_template("index.html", cities=city_names)

@app.route("/<city_name>")
def weather(city_name):
    try:
        html_current, html_3days = weather_dashboard(city_name)
    except RuntimeError as e:
        return render_template("city_name.html", city=city_name, error=str(e)), 502
    return render_template("city_name.html", city=city_name, dashboard=html_3days, current_weather = html_current)
