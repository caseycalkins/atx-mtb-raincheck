import json
from authenticate.auth import TwitterAuth
from dotenv import load_dotenv
import os
load_dotenv()

WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")
PATH = "data/trails.json"

# Create twitter auth object
twitter_auth = TwitterAuth()
# Get the api object
api = twitter_auth.get_api()
# Update status
# api.update_status("Hi")

def parse_trail_data_file() -> dict:
    with open(PATH, "r") as trail_data:
        data = json.load(trail_data)
        for trail in data:
            return data[trail]


def fetch_weather_data() -> str:
    trail_data = parse_trail_data_file()
    return
    

def format_tweet_with_weather_data():
    with open(PATH, "r") as trail_data:
        data = json.load(trail_data)
        # print(data["trails"]["walnut_creek"])
        return
            


fetch_weather_data()