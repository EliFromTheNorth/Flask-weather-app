import logging

from flask import Flask, redirect, render_template, request, url_for

from api import WeatherAPIError
from weather_service import city_name_list, weather_dashboard, forecast_title

# Loggning till konsolen, så att man ser vad som händer i appen
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Registrerar filtret så att det kan användas i mallarna
app.add_template_filter(forecast_title, "forecast_title")


@app.errorhandler(404)
def error404(error):
    return render_template("error404.html"), 404


@app.route("/")
def index():
    # Formuläret skickar valet som selected_city
    selected_city = request.args.get("selected_city")
    if selected_city:
        # Skicka vidare till prognossidan för den valda staden
        return redirect(url_for("weather", city_name=selected_city))
    try:
        city_names = city_name_list()
    except WeatherAPIError as e:
        return render_template("index.html", cities=[], error=str(e)), 502
    return render_template("index.html", cities=city_names)


@app.route("/<city_name>")
def weather(city_name):
    try:
        # Hämtar data och bygger tabellerna. Okänd stad ger 404 (abort i weather_service)
        html_current, html_3days = weather_dashboard(city_name)
    except WeatherAPIError as e:
        return render_template("city_name.html", city=city_name, error=str(e)), 502
    return render_template(
        "city_name.html",
        city=city_name,
        dashboard=html_3days,
        current_weather=html_current,
    )
