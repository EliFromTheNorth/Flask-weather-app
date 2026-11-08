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