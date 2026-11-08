from unittest.mock import Mock, patch

import pytest
import requests

from api import WeatherAPIError, fetch_weather


# Lyckat fall: requests.get mockas, så inget nätverk behövs. Funktionen ska returnera JSON-data
@patch("api.requests.get")
def test_fetch_ok(mock_get):
    mock_get.return_value.json.return_value = {"a": 1}
    assert fetch_weather("https://invalid-adress-12345") == {"a": 1}


# Felfall: timeout ska bli vårt eget fel WeatherAPIError med meddelandet "Timeout"
@patch("api.requests.get", side_effect=requests.Timeout)
def test_timeout(mock_get):
    with pytest.raises(WeatherAPIError, match="Timeout"):
        fetch_weather("https://invalid-adress-12345")


# Felfall: servern går inte att nå (ConnectionError)
@patch("api.requests.get", side_effect=requests.ConnectionError)
def test_connection(mock_get):
    with pytest.raises(WeatherAPIError, match="internet connection"):
        fetch_weather("https://invalid-adress-12345")


# Felfall: övriga fel från requests fångas av det sista, allmänna except-blocket
@patch("api.requests.get", side_effect=requests.RequestException)
def test_other_request_error(mock_get):
    with pytest.raises(WeatherAPIError, match="An error"):
        fetch_weather("https://invalid-adress-12345")


# Felfall: HTTP-fel (t.ex. 401) från API:et. Statuskoden ska finnas i meddelandet
@patch(
    "api.requests.get", side_effect=requests.HTTPError(response=Mock(status_code=401))
)
def test_http_error(mock_get):
    with pytest.raises(WeatherAPIError, match="401"):
        fetch_weather("https://invalid-adress-12345")
