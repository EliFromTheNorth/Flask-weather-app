import logging

import pandas as pd
from flask import abort

from api import fetch_weather

# Loggning till konsolen
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

URL = "https://api.open-meteo.com/v1/forecast?latitude=59.3294,55.6059,57.71,63.8284,67.8557&longitude=18.0687,13.0007,11.97,20.2597,20.2251&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&current=temperature_2m,wind_speed_10m&timezone=auto&forecast_days=3"

cities_list = {
    "Stockholm": {"lat": 59.33, "lon": 18.07},
    "Göteborg": {"lat": 57.71, "lon": 11.97},
    "Malmö": {"lat": 55.61, "lon": 13.0},
    "Umeå": {"lat": 63.83, "lon": 20.26},
    "Kiruna": {"lat": 67.86, "lon": 20.22},
}


def cities(url):
    # API:et svarar med en lista, en post per plats, men utan stadsnamn
    data = fetch_weather(url)

    cities_json = []
    for e in data:
        # Avrundar koordinaterna så att de kan jämföras med cities_list
        lat = round(e["latitude"], 2)
        lon = round(e["longitude"], 2)
        city_found = False
        for city in cities_list:
            # Matchar koordinaterna mot en stad och lägger till stadsnamnet i svaret
            if lat == cities_list[city]["lat"] and lon == cities_list[city]["lon"]:
                e["city"] = city
                cities_json.append(e)
                city_found = True
                break
        if not city_found:
            logger.warning(f"City with long {lon} and lat {lat} not found.")

    return cities_json


# Tar ut bara stadsnamnen, som används i rullgardinslistan
def city_name_list():
    cities_json = cities(URL)
    city_names = []
    for e in cities_json:
        city_names.append(e["city"])
    return city_names


# Ingen nätverksanrop, därför enkel att testa med parametrize
def is_valid_city(name):
    """Return True if the city is in our list."""
    return name in cities_list


def select_city(city_name):
    # Okänd stad: svara med 404 direkt, innan vi ens anropar API:et
    if not is_valid_city(city_name):
        abort(404)
    data = cities(URL)
    for e in data:
        if e["city"] == city_name:
            logger.info(f"City {city_name} found.")
            return e
    # Staden finns i listan men inte i API-svaret
    logger.warning(f"City {city_name} not found.")
    abort(404)


# Bygger en tabell med nuvarande temperatur och vind för vald stad
def current_weather_table(city):
    table_data = []
    selected_city = select_city(city)
    if selected_city:
        table_data.append(
            {
                "Temperature": f"{selected_city['current']['temperature_2m']} {selected_city['current_units']['temperature_2m']}",
                "Wind speed": f"{selected_city['current']['wind_speed_10m']} {selected_city['current_units']['wind_speed_10m']}",
            }
        )
        # .T vänder tabellen så att värdena hamnar på rader
        df = pd.DataFrame(table_data).T
    else:
        df = None
    return df


# Bygger tabellen för tre dagar: en rad per dag med datum, nederbörd, max och min
def create_table_3days(city):
    table_data = []
    selected_city = select_city(city)
    if selected_city:
        for i in range(len(selected_city["daily"]["time"])):
            table_data.append(
                {
                    "": selected_city["daily"]["time"][i],
                    "Daily precipitation": f"{selected_city['daily']['precipitation_sum'][i]} {selected_city['daily_units']['precipitation_sum']}",
                    "max daily temperature": f"{selected_city['daily']['temperature_2m_max'][i]} {selected_city['daily_units']['temperature_2m_max']}",
                    "min daily temperature": f"{selected_city['daily']['temperature_2m_min'][i]} {selected_city['daily_units']['temperature_2m_min']}",
                }
            )
        # .T vänder tabellen så att värdena hamnar på rader
        df = pd.DataFrame(table_data).T
    else:
        df = None
    return df


# Samlar båda tabellerna och gör om dem till HTML som mallen kan visa
def weather_dashboard(city):
    current_table = current_weather_table(city)
    table = create_table_3days(city)
    if table is not None and current_table is not None:
        html_3days = table.to_html(classes="table table-striped", header=False)
        html_current = current_table.to_html(
            classes="table table-striped", header=False
        )
        return html_current, html_3days
    return None, None
