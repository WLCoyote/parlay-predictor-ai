# src/api/odds_api.py
import requests
import time
from src.utils.config import ODDS_API_KEY

# REAL EVENT ID FOR Raiders @ Broncos TNF (Nov 6, 2025)
TNF_EVENT_ID = "13bdffda97e8fb13179fe3f2f69d66f8"

def get_upcoming_events_with_props():
    return [{
        "id": TNF_EVENT_ID,
        "home": "Denver Broncos",
        "away": "Las Vegas Raiders",
        "commence_time": "2025-11-06"
    }]

def get_player_props(event_id=TNF_EVENT_ID):
    url = f"https://api.the-odds-api.com/v4/sports/americanfootball_nfl/events/{event_id}/odds"
    params = {
        "apiKey": ODDS_API_KEY,
        "regions": "us",
        "markets": "player_pass_yds",  # Passing yards (real, live right now)
        "oddsFormat": "american",
        "bookmakers": "draftkings"
    }
    
    try:
        time.sleep(3)
        response = requests.get(url, params=params, timeout=20)
        print(f"PROPS STATUS: {response.status_code}")
        if response.status_code != 200:
            return []
        data = response.json()
        props = []
        for market in data.get("markets", []):
            for outcome in market.get("outcomes", []):
                if outcome.get("name") == "Over":
                    player = outcome.get("description")
                    point = outcome.get("point")
                    odds = outcome.get("price")
                    props.append({
                        "player": player,
                        "prop": f"Over {point} passing yds",
                        "odds": odds,
                        "book": "DraftKings"
                    })
        print(f"REAL PASSING PROPS FOUND: {len(props)}")
        return props[:10]
    except Exception as e:
        print(f"Error: {e}")
        return []