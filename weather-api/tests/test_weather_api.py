from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_read_weather():
    """
    Test the /weather endpoint without filters.
    Expected: Returns a 200 status code and a list of weather data.
    """
    response = client.get("/api/v1/weather/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_read_weather_with_filters():
    """
    Test the /weather endpoint with station_id and date filters.
    Expected: Returns a 200 status code and a filtered list of weather data.
    """
    response = client.get("/api/v1/weather/?station_id=USC00113335&date=1985-01-19")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_weather_stats():
    """
    Test the /weather/stats endpoint without filters.
    Expected: Returns a 200 status code and a list of weather stats.
    """
    response = client.get("/api/v1/weather/stats")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_weather_stats_with_filters():
    """
    Test the /weather/stats endpoint with station_id and year filters.
    Expected: Returns a 200 status code and a filtered list of weather stats.
    """
    response = client.get("/api/v1/weather/stats?station_id=USC00110072&year=2020")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
