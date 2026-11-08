from unittest.mock import Mock, patch
from weather_service import current_weather_table, city_name_list

fake_current_weather_data = [{
    "latitude": 59.33,
    "longitude": 18.07,
    "city": "Stockholm",
    "current": {
            "temperature_2m": 36,
        "wind_speed_10m": 2
    }}]

       
@patch("weather_service.data", fake_current_weather_data)
def test_current_weather_table():
    table = current_weather_table("Stockholm")
    assert len(table) == 2
    assert table.iloc[0, 0] == 36
    assert table.iloc[1, 0] == 2

def test_correct_cities_json():
    expected_data = {'Stockholm', 'Göteborg', 'Malmö', 'Umeå', 'Kiruna'}
    assert set(city_name_list()) == expected_data

