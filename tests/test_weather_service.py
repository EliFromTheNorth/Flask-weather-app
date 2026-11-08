from unittest.mock import Mock, patch
from weather_service import current_weather_table, city_name_list, is_valid_city
import pytest

fake_current_weather_data = {
    # "latitude": 59.33,
    # "longitude": 18.07,
    "city": "Stockholm",
    "current": {
        "temperature_2m": 36,
        "wind_speed_10m": 2},
    "current_units": {
        "temperature_2m": "°C", 
        "wind_speed_10m": "km/h"},
    }

       
@patch("weather_service.select_city", return_value=fake_current_weather_data)
def test_current_weather_table(mock_select):
    table = current_weather_table("Stockholm")
    assert len(table) == 2
    assert table.iloc[0, 0] == "36 °C"
    assert table.iloc[1, 0] == "2 km/h"

@patch(
    "weather_service.cities",
    return_value=[
        {"city": "Stockholm"},
        {"city": "Göteborg"},
        {"city": "Malmö"},
        {"city": "Umeå"},
        {"city": "Kiruna"},
    ],
)
def test_correct_cities_json(mock_cities):
    expected_data = {"Stockholm", "Göteborg", "Malmö", "Umeå", "Kiruna"}
    assert set(city_name_list()) == expected_data


@pytest.mark.parametrize(
    "name, expected",
    [("Stockholm", True), ("Kiruna", True), ("Paris", False), ("", False)],
)
def test_is_valid_city(name, expected):
    assert is_valid_city(name) == expected

