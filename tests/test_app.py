# from api import cities

# def test_correct_cities():
#     expected_data = {'Stockholm', 'Göteborg', 'Malmö', 'Umeå', 'Kiruna'}
#     assert set(cities) == expected_data
#     assert len(cities) == 5

from weather_service import cities
def test_correct_cities_json():
    url = "https://api.open-meteo.com/v1/forecast?latitude=59.3294,55.6059,57.71,63.8284,67.8557&longitude=18.0687,13.0007,11.97,20.2597,20.2251&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&current=temperature_2m,wind_speed_10m&timezone=auto&forecast_days=3"
    expected_data = {'Stockholm', 'Göteborg', 'Malmö', 'Umeå', 'Kiruna'}
    assert set(cities(url)) == expected_data
    assert len(cities(url)) == 5