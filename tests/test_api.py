import pytest
import requests
from unittest.mock import patch, Mock
from api import fetch_weather


@patch("api.requests.get", side_effect=requests.Timeout)
def test_timeout(mock_get):
    with pytest.raises(WeatherAPIError, match="Timeout"):
        fetch_weather("https://invalid-adress-12345")

@patch("api.requests.get", side_effect=requests.ConnectionError)
def test_connection(mock_get):
    with pytest.raises(WeatherAPIError, match="internet connection"):
            fetch_weather("https://invalid-adress-12345")

@patch("api.requests.get", side_effect=requests.RequestException)
def test_other_request_error(mock_get):
    with pytest.raises(WeatherAPIError, match="An error"):
        fetch_weather("https://invalid-adress-12345")

@patch("api.requests.get", side_effect=requests.HTTPError(response=Mock(status_code=401)))
def test_http_error(mock_get):
    with pytest.raises(WeatherAPIError, match="401"):
        fetch_weather("https://invalid-adress-12345")