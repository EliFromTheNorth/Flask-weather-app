# from api import cities

# def test_correct_cities():
#     expected_data = {'Stockholm', 'Göteborg', 'Malmö', 'Umeå', 'Kiruna'}
#     assert set(cities) == expected_data
#     assert len(cities) == 5

# from weather_service import cities
# def test_correct_cities_json():
#     url = "https://api.open-meteo.com/v1/forecast?latitude=59.3294,55.6059,57.71,63.8284,67.8557&longitude=18.0687,13.0007,11.97,20.2597,20.2251&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&current=temperature_2m,wind_speed_10m&timezone=auto&forecast_days=3"
#     expected_data = {'Stockholm', 'Göteborg', 'Malmö', 'Umeå', 'Kiruna'}
#     assert set(cities(url)) == expected_data
#     assert len(cities(url)) == 5

from unittest.mock import patch

import pytest
from werkzeug.exceptions import NotFound

from api import WeatherAPIError
from app import app



@pytest.fixture
def client():
    return app.test_client()


@patch("app.city_name_list", return_value=["Stockholm", "Kiruna"])
def test_index_ok(mock_cities, client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Stockholm" in response.get_data(as_text=True)


@patch("app.weather_dashboard", side_effect=NotFound)
def test_unknown_city_gives_404(mock_dashboard, client):
    assert client.get("/Paris").status_code == 404


@patch("app.weather_dashboard", side_effect=WeatherAPIError("API is down"))
def test_api_error_shows_message(mock_dashboard, client):
    response = client.get("/Malmö")
    assert response.status_code == 502
    assert "API is down" in response.get_data(as_text=True)