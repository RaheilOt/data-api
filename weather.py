# pylint: disable=missing-module-docstring

import sys
import urllib.parse
import requests

BASE_URI = "https://weather.lewagon.com"


def search_city(query):
    """
    Look for a given city using the API.
    If multiple options are returned, ask the user to choose one.
    Return a dictionary with city info or None if not found.
    """
    url = f"{BASE_URI}/geo/1.0/direct?q={urllib.parse.quote(query)}&limit=5"
    response = requests.get(url, timeout=5).json()

    if not response:
        print("City not found, please try again.")
        return None

    if len(response) == 1:
        return response[0]

    # Multiple matches found
    print("Multiple matches found, which city did you mean?")
    for idx, city in enumerate(response, start=1):
        print(f"{idx}. {city['name']},{city.get('country','')}")
    choice = int(input("> "))
    return response[choice - 1]


def weather_forecast(lat, lon):
    """
    Return a 5-day weather forecast for the city given its latitude and longitude.
    Each day's forecast is a dictionary with date, weather description, and max temp.
    """
    url = f"{BASE_URI}/data/2.5/forecast?lat={lat}&lon={lon}&units=metric"
    response = requests.get(url, timeout=5).json()
    forecasts = response.get("list", [])

    daily_forecast = []
    seen_dates = set()
    for f in forecasts:
        date = f['dt_txt'].split(" ")[0]
        if date not in seen_dates:
            daily_forecast.append({
                "date": date,
                "weather": f['weather'][0]['description'],
                "max_temp": f['main']['temp_max']
            })
            seen_dates.add(date)
        if len(daily_forecast) == 5:
            break
    return daily_forecast


def main():
    """
    Ask the user for a city and display the weather forecast.
    """
    query = input("City?\n> ")
    city = search_city(query)
    if not city:
        return

    forecasts = weather_forecast(city['lat'], city['lon'])
    print(f"Here's the weather in {city['name']}")
    for day in forecasts:
        print(f"{day['date']}: {day['weather'].capitalize()} {day['max_temp']}°C")


if __name__ == '__main__':
    try:
        while True:
            main()
    except KeyboardInterrupt:
        print('\nGoodbye!')
        sys.exit(0)
