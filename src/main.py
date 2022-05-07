import json
import os
import pprint
from datetime import datetime, time, timedelta

import requests
from dotenv import load_dotenv

from authenticate.auth import TwitterAuth

load_dotenv()

WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")
PATH = "data/trails.json"

# Create twitter auth object
twitter_auth = TwitterAuth()
# Get the api object
api = twitter_auth.get_api()
# Update status
# api.update_status("Hi")

def get_yesterdays_midnight() -> datetime:   
    last_midnight = datetime.combine(datetime.now(), time.min)
    return (last_midnight - timedelta(days=1)).strftime('%s')


def parse_trail_data_file() -> dict:
    with open(PATH, "r") as trail_data:
        data = json.load(trail_data)
        for trail in data:
            return data[trail]


def fetch_weather_data() -> str:
    trail_data = parse_trail_data_file()
    yesterdays_midnight = get_yesterdays_midnight()
    for trail, coords in trail_data.items():
        url = f"https://api.openweathermap.org/data/2.5/onecall/timemachine?lat={coords['lat']}&lon={coords['long']}&dt={yesterdays_midnight}&appid={WEATHER_API_KEY}&units=imperial"
        r = requests.get(url)
        if r.status_code == 200:
            pprint.pprint(r.json())
    

def format_tweet_with_weather_data():
    with open(PATH, "r") as trail_data:
        data = json.load(trail_data)
        return

