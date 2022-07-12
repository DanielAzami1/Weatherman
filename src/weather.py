import geocoder
import requests
from loguru import logger
import utils


def find_my_location(latlng_required: bool = True) -> list:
    """
    :param latlng_required: (bool) specify whether to return latitude/longitude or standard location description,
    for weather api call.
    :return: [list] user's current location.
    """
    g = geocoder.ip('me')
    if latlng_required:
        return g.latlng, g.current_result
    else:
        return g.current_result


def grab_weather_info(lat, lon, geo_location, units='imperial', api_key=None) -> str:
    """
    :param lat: (float) latitude of requester
    :param lon: (float) longitude of requester
    :param geo_location: (geoid obj) plaintext location of requester (e.g., [city, state, country])
    :param units: (str) units to display temps in (e.g., imperial, standard [default], metric)
    :param api_key: (str) api key imported from config.py
    :return: (str) weather report
    """
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units={units}&appid={api_key}"
    request_timestamp = utils.get_current_time() + ", " + utils.get_current_date()
    logger.info(f'Requesting weather report for user in {geo_location}, at {request_timestamp}')
    response = requests.get(url).json()
    weather_info = {
        'weather': response['weather'][0],  # this dict was nested in a list for some reason
        'main': response['main'],
        'visibility': response['visibility'],
        'wind': response['wind'],
        'clouds': response['clouds']
    }
    geo_location = str(geo_location)[1:-1]  # cast to str and remove brackets
    payload = f"Weather report [{geo_location}, {utils.get_current_time()}]\n" \
              f"{weather_info['weather']['main']} - {weather_info['weather']['description']}, " \
              f"{weather_info['main']['temp']}(F), High: {weather_info['main']['temp_max']}(F)," \
              f" Low: {weather_info['main']['temp_min']}(F), Humidity: {weather_info['main']['humidity']}%"
    logger.success(f'Weather report generated successfully at {utils.get_current_time()}')
    return payload


def generate_weather_report() -> str:
    """Essentially a wrapper for the two methods above"""
    (latitude, longitude), location = find_my_location(latlng_required=True)
    from config import API_KEY
    weather_report = grab_weather_info(lat=latitude, lon=longitude, geo_location=location, api_key=API_KEY)
    return weather_report
