from unittest.mock import patch

import pytest

from weather_service import city_name_list, current_weather_table, is_valid_city

# Låtsasdata för en stad, så att testet inte behöver något nätverk
fake_current_weather_data = {
    "city": "Stockholm",
    "current": {"temperature_2m": 36, "wind_speed_10m": 2},
    "current_units": {"temperature_2m": "°C", "wind_speed_10m": "km/h"},
}


# tabellen ska ha två rader (temperatur och vind) med enheter.
# select_city mockas, så inget API-anrop görs
@patch("weather_service.select_city", return_value=fake_current_weather_data)
def test_current_weather_table(mock_select):
    table = current_weather_table("Stockholm")
    assert len(table) == 2
    assert table.iloc[0, 0] == "36 °C"
    assert table.iloc[1, 0] == "2 km/h"


# city_name_list ska returnera alla fem stadsnamn.
# cities mockas med ett färdigt svar, så testet körs utan nätverk
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


# parametrize kör samma test flera gånger med olika indata.
# täcker både giltiga städer och felfall (okänd stad, tom sträng)
@pytest.mark.parametrize(
    "name, expected",
    [("Stockholm", True), ("Kiruna", True), ("Paris", False), ("", False)],
)
def test_is_valid_city(name, expected):
    assert is_valid_city(name) == expected
