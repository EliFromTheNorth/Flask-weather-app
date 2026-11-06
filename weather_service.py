from api import fetch_weather
import requests
import json

url = "https://api.open-meteo.com/v1/forecast?latitude=59.3294,55.6059,57.71,63.8284,67.8557&longitude=18.0687,13.0007,11.97,20.2597,20.2251&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&current=temperature_2m,wind_speed_10m&timezone=auto&forecast_days=3"

cities_list = {
    "Stockholm": {"lat": 59.33, "lon": 18.07},
    "Göteborg": {"lat": 57.71, "lon": 11.97},
    "Malmö": {"lat": 55.61, "lon": 13.0},
    "Umeå": {"lat": 63.83, "lon": 20.26},
    "Kiruna": {"lat": 67.86, "lon": 20.22}
}

def cities(url):
    data = fetch_weather(url)

    cities_json = []
    # test = []
    for e in data:
        # e['city'] = ""
        lat = round(e['latitude'], 2)
        lon = round(e['longitude'], 2)
        for city in cities_list:
            if lat == cities_list[city]['lat'] and lon == cities_list[city]['lon']:
                # e['city'] = city
                # cities_json.append(e)
                ordered_city_data = {"city": city, **e}
                
                cities_json.append(ordered_city_data)
        # test.append(lat)
        # test.append(lon)

    # return test
    # return cities_json
    city_names = []
    for e in cities_json:
        city_names.append(e['city'])

    return city_names


# print(cities(url))

pretty_data = json.dumps(cities(url), indent=4, ensure_ascii=False)
print(pretty_data)

