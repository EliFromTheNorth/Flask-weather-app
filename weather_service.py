from api import fetch_weather
# import requests
# import json
from pprint import pprint
import logging
import pandas as pd
from flask import abort 

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


# pprint(cities(URL))

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
    abort(404)
        

pprint(select_city('Stockholm'))
# pprint(select_city('hhh'))

# def units(number, key, city):
#     selected_city = select_city(city)
    
#     if key in selected_city.get('current', {}):
#         unit = selected_city.get('current_units', {}).get(key, '')
#         return f"{number} {unit}"
        
#     elif key in selected_city.get('daily', {}):
#         unit = selected_city.get('daily_units', {}).get(key, '')
#         return f"{number} {unit}"
        
#     return number

# def units(number, key, city):
#     selected_city = select_city(city)
#     if not selected_city:
#         return number

#     # Pokud klíč obsahuje slovo 'temperature', přidáme °C (nebo jednotku přímo z API)
#     if 'temperature' in key.lower():
#         # Zkusíme najít jednotku v current_units nebo daily_units
#         unit = selected_city.get('current_units', {}).get(key, '')
#         if not unit:
#             unit = selected_city.get('daily_units', {}).get(key, '')
        
#         # Pojistka kdyby v JSONu jednotka nebyla, natvrdo dáme °C
#         if not unit:
#             unit = "°C"
            
#         return f"{number} {unit}"
        
#     return number

def current_weather_table(city):
    table_data = []
    selected_city = select_city(city)
    if selected_city:
        table_data.append({
            "Temperature": f"{selected_city['current']['temperature_2m']} {selected_city['current_units']['temperature_2m']}",
            "Wind speed": f"{selected_city['current']['wind_speed_10m']} {selected_city['current_units']['wind_speed_10m']}"
        })
        df = pd.DataFrame(table_data).T
    else:
        df = None
    return df


def create_table_3days(city):
    table_data = []
    selected_city = select_city(city) # tady se vybere to mesto, ketre uzivatel vybrala poslou se vsechny data k tomu mestu
    if selected_city:
        for i in range(len(selected_city['daily']['time'])):
            table_data.append({
                "datum": selected_city['daily']['time'][i],
                "Daily precipitation": f"{selected_city['daily']['precipitation_sum'][i]} {selected_city['daily_units']['precipitation_sum']}",
                "max daily temperature": f"{selected_city['daily']['temperature_2m_max'][i]} {selected_city['daily_units']['temperature_2m_max']}",
                "min daily temperature": f"{selected_city['daily']['temperature_2m_min'][i]} {selected_city['daily_units']['temperature_2m_min']}"
            })
        df = pd.DataFrame(table_data).T
    else:
        df = None
    return df #vrati tabulku k danemu mestu

# print(create_table("Stockholm"))




def weather_dashboard(city):
    current_table = current_weather_table(city)
    table = create_table_3days(city)
    # table.columns = ["" for _ in table.columns]
    # if df_current is not None and table_3days is not None:
    if table is not None and current_table is not None:
        html_3days = table.to_html(classes="table table-striped", header=False)
        html_current = current_table.to_html(classes="table table-striped", header=False)
        return html_current, html_3days
    return None, None 