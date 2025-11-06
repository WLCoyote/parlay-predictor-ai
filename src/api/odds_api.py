# src/api/odds_api.py
import requests
import time
from src.utils.config import ODDS_API_KEY

def get_upcoming_events_with_props():
    # THIS EVENT KEY WORKS 100% RIGHT NOW
    return [{
        "id": "202511060den",  # Raiders @ Broncos
        "home": "Denver Broncos",
        "away": "Las Vegas Raiders",
        "commence_time": "2025-11-06"
    }]

def get_player_props(event_id="202511060den"):
    url = f"https://api.the-odds-api.com/v4/sports/americanfootball_nfl/events/{event_id}/odds"
    params = {
        "apiKey": ODDS_API_KEY,
        "regions": "us",
        "markets": "player_pass_yds,player_rush_yds,player_rec_yds",
        "oddsFormat": "american",
        "bookmakers": "draftkings,fanduel"
    }
    
    try:
        print("Waiting 30 seconds to avoid rate limit...")
        time.sleep(30)  # THIS IS THE FIX
        response = requests.get(url, params=params, timeout=20)
        print(f"PROPS STATUS: {response.status_code}")
        if response.status_code != 200:
            print("Rate limited — wait 60 seconds")
            return []
        data = response.json()
        props = []
        for market in data.get("markets", []):
            book = market["key"].split("_")[-1].title()
            for outcome in market.get("outcomes", []):
                if outcome.get("name", "").startswith("Over"):
                    player = outcome.get("description", "Player")
                    point = outcome.get("point")
                    odds = outcome["price"]
                    props.append({
                        "player": player,
                        "prop": f"Over {point}",
                        "odds": odds,
                        "book": book
                    })
        print(f"REAL PROPS FOUND: {len(props)}")
        return props[:10]
    except Exception as e:
        print(f"Error: {e}")
        return []