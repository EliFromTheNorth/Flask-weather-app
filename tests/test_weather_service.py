from unittest.mock import Mock, patch
from weather_service import current_weather_table

fake_current_weather_data = {
        "current": {
             "temperature_2m": 36,
            "wind_speed_10m": 2
        }}

       
@patch("api.requests.get")
def test_current_weather_table(mock_get):
    mock_get.return_value = Mock(
        status_code=200,
        json=lambda: fake_current_weather_data,
    )
    table = current_weather_table("url")
    assert len(table) == 2
    assert table.iloc[0]["Temperature"] == 36
    assert table.iloc[1]["Wind speed"] == 2



