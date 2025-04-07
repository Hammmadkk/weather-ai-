import requests
from geopy.geocoders import Nominatim

def get_lat_long(location_name):
    geolocator = Nominatim(user_agent="geoapi")
    location = geolocator.geocode(location_name)
    return location.latitude, location.longitude

def get_weather(location_name):
    lat,lon = get_lat_long(location_name)
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m"

    response = requests.get(url)
    response = response.json()
    pretty_response = f"Current Temperature in {location_name} is {response['current']['temperature_2m']}°C."
    return pretty_response
    