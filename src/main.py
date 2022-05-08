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
PATH = "data/trails.json"

# Create twitter auth object
twitter_auth = TwitterAuth()
# Get the api object
api = twitter_auth.get_api()
# Update status
# api.update_status("Hi")

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

    for trail, coords in trail_data.items():
        url = f"https://api.weatherapi.com/v1/history.json?key={WEATHER_API_KEY}&q={coords['lat']},{coords['long']}&dt={yesterdays_date}"
        r = requests.get(url)
        if r.status_code == 200:
            trail_weather_data[trail] = r.json()["forecast"]["forecastday"][0]["day"]["totalprecip_in"]
            
    pprint.pprint(trail_weather_data)
       

def format_tweet_with_weather_data():
    with open(PATH, "r") as trail_data:
        data = json.load(trail_data)
        return

