from api import cities
def test_correct_cities():
    expected_data = {Stockholm, Göteborg, Malmö, Umeå, Kiruna}
    assert set(cities) == expected_data
    assert len(cities) == 5