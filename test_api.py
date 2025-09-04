# pylint: disable=missing-docstring,invalid-name
import requests
# Simple test to check API call to Le Wagon weather proxy
url = "https://weather.lewagon.com/geo/1.0/direct?q=Barcelona"
response = requests.get(url, timeout=5).json()  # Added timeout
city = response[0]
print(f"{city['name']}: ({city['lat']}, {city['lon']})")
