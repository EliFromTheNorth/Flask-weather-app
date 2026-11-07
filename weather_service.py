from api import fetch_weather
# import requests
# import json
from pprint import pprint
import logging
import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

URL = "https://api.open-meteo.com/v1/forecast?latitude=59.3294,55.6059,57.71,63.8284,67.8557&longitude=18.0687,13.0007,11.97,20.2597,20.2251&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&current=temperature_2m,wind_speed_10m&timezone=auto&forecast_days=3"

cities_list = {
    "Stockholm": {"lat": 59.33, "lon": 18.07},
    "Göteborg": {"lat": 57.71, "lon": 11.97},
    "Malmö": {"lat": 55.61, "lon": 13.0},
    "Umeå": {"lat": 63.83, "lon": 20.26},
    "Kiruna": {"lat": 67.86, "lon": 20.22}
}

def cities(url):
    data = fetch_weather(URL)

    cities_json = []
    for e in data:
        lat = round(e['latitude'], 2)
        lon = round(e['longitude'], 2)
        city_found = False
        for city in cities_list:
            if lat == cities_list[city]['lat'] and lon == cities_list[city]['lon']:
                e['city'] = city
                cities_json.append(e)
                # ordered_city_data = {"city": city, **e}                
                # cities_json.append(ordered_city_data)
                city_found = True
                break
        if not city_found:
            logger.warning(f"City with long {lon} and lat {lat} not found.")

    return cities_json

def city_name_list():
    cities_json = cities(URL)
    city_names = []
    for e in cities_json:
        city_names.append(e['city'])
    return city_names
# return sorted(list({e['city'] for e in cities_json if 'city' in e}))


# pprint(cities(url))

# pretty_data = json.dumps(cities(url), indent=4, ensure_ascii=False)
# print(pretty_data)

data = cities(URL)

#tady do te funkce se bude posilat to mesto, ktere uzivatel vybral v roletce
def select_city(city_name):
    for e in data:
        if e['city'] == city_name:
            logger.info(f"City {city_name} found.")
            return e
    logger.warning(f"City {city_name} not found.")
    return None
        

# pprint(select_city('Stockholm'))
# pprint(select_city('hhh'))


def create_table(city): #casem se to predela na dve tabulky
    table_data = []
    # selected_city = select_city("Stockholm") #TEST
    selected_city = select_city(city) # tady se vybere to mesto, ketre uzivatel vybrala poslou se vsechny data k tomu mestu
    if selected_city:
        for i in range(len(selected_city['daily']['time'])):
            if i == 0:
                current_temp = selected_city['current']['temperature_2m']
                current_wind = selected_city['current']['wind_speed_10m']
            else:
                current_temp = "" 
                current_wind = ""
            table_data.append({
                "datum": selected_city['daily']['time'][i],
                "Temperatur": current_temp,
                "Wind speed": current_wind,
                "Daily precipitation": selected_city['daily']['precipitation_sum'][i],
                "max daily temperature": selected_city['daily']['temperature_2m_max'][i],
                "min daily temperature": selected_city['daily']['temperature_2m_min'][i]
            })
        df = pd.DataFrame(table_data).T
    else:
        df = None
    return df #vrati tabulku k danemu mestu

# print(create_table("Stockholm"))

def weather_dashboard(city):
    table = create_table(city) #tady by se asi melo dat to mesto, ktere uzivatel vybere?
    # table.columns = ["" for _ in table.columns]
    html = table.to_html(classes="table table-striped", header=False)
    return html