import json
import os
import pprint
import random
from datetime import datetime, time, timedelta

import requests
from dotenv import load_dotenv

from authenticate.twitter_auth import TwitterAuth

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
PATH = "sr/data/trails.json"

TW_AUTH = TwitterAuth()
TW_API = TW_AUTH.get_api()


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

    for trail, coords in trail_data.items():
        try:
            current_weather_request = requests.get(current_url.format(WEATHER_API_KEY, coords['lat'], coords['long'])).json()
            current_rain_amount = current_weather_request["current"]["precip_in"]
            history_weather_request = requests.get(history_url.format(WEATHER_API_KEY, coords['lat'], coords['long'], yesterdays_date)).json()
            historical_rain_amount = history_weather_request["forecast"]["forecastday"][0]["day"]["totalprecip_in"]

            if current_rain_amount > 0:
                trail_weather_data[trail] = f"may be experiencing rain. {current_rain_amount} inches recently detected."
            elif historical_rain_amount > 0:
                trail_weather_data[trail] = f"May be wet. {historical_rain_amount} inches of rain detected within the last 24hrs."
            else:
                trail_weather_data[trail] = "No rain detected, have fun!"
        except Exception as e:
            print(e)
    return trail_weather_data
   

def format_and_send_tweet():
    hash_tags = ["#trails", "#hiking", "#mtb", "#mtbtrails", "#mountainbiking", "#austin", "#atx", "#atxmtb", "#sendit", "#XC", "#xc", "#downhill", "#downhill_mtb", "#cycling", "#shred", "#shredit", "#bikelife", "#bicycle", "#singletrack", "#mtbs", "#gmbn", "#localtrail", "#enduro", "#race", "#racing"]
    to_tweet = ""
    trail_weather_data = fetch_weather_data()
    get_random_hashtag = random.choice(hash_tags)

    for trail, status in trail_weather_data.items():
        formatted_trail = trail.replace("_", " ").title()
        to_tweet += f"{formatted_trail}: {status}\n"
        if len(to_tweet) + len(formatted_trail) + len(status) + len(max(get_random_hashtag, key=len)) > 280:
            TW_API.update_status(status=to_tweet + get_random_hashtag)
            to_tweet = ""
    if to_tweet:
        TW_API.update_status(status=to_tweet + get_random_hashtag)

    
if __name__ == "__main__":
    format_and_send_tweet()
