import json
import os
import pprint
import time as time_
from datetime import datetime, time, timedelta

import requests
from dotenv import load_dotenv

from authenticate.twitter_auth import TwitterAuth

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
PATH = "data/test_data.json"


def get_yesterdays_date() -> datetime:   
    last_midnight = datetime.combine(datetime.now(), time.min)
    return (last_midnight - timedelta(days=1)).strftime('%Y-%m-%d')


def parse_trail_data_file() -> dict:
    trail_coordinates = {}
    with open(PATH, "r") as trail_data:
        data = json.load(trail_data)
        for trail, coords in data.items():
            trail_coordinates[trail] = coords
    return trail_coordinates
            
           
def fetch_weather_data() -> dict:
    trail_weather_data = {}
    trail_data = parse_trail_data_file()
    yesterdays_date = get_yesterdays_date()
    history_url = "https://api.weatherapi.com/v1/history.json?key={}&q={},{}&dt={}"
    current_url = "https://api.weatherapi.com/v1/current.json?key={}&q={},{}&aqi=no"

    prep_for_tweet = {}
    for trail, coords in trail_data.items():
        try:
            current_weather_request = requests.get(current_url.format(WEATHER_API_KEY, coords['lat'], coords['long'])).json()
            current_rain_amount = current_weather_request["current"]["precip_in"]
            history_weather_request = requests.get(history_url.format(WEATHER_API_KEY, coords['lat'], coords['long'], yesterdays_date)).json()
            historical_rain_amount = history_weather_request["forecast"]["forecastday"][0]["day"]["totalprecip_in"]

            if current_weather_request["current"]["precip_in"] > 0:
                print(f"{trail} may be experiencing rain. {current_rain_amount} inches recently detected.")
            elif history_weather_request["forecast"]["forecastday"][0]["day"]["totalprecip_in"] > 0:
                print(f"{trail} may be wet. {historical_rain_amount} inches of rain within the last 24hrs.")
        except Exception as e:
            print(e)

            
   
def format_tweet_with_weather_data():
    with open(PATH, "r") as trail_data:
        data = json.load(trail_data)
        return

fetch_weather_data()

# Create twitter auth object
twitter_auth = TwitterAuth()
# Get the api object
api = twitter_auth.get_api()
# Update status
# api.update_status("Hi")


