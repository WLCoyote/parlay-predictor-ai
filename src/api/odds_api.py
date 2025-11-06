# src/api/odds_api.py
import requests
import time
from src.utils.config import ODDS_API_KEY

def get_upcoming_events_with_props():
    url = (
        "https://api.the-odds-api.com/v4/sports/americanfootball_nfl/odds?"
        f"apiKey={ODDS_API_KEY}"
        "&regions=us"
        "&markets=h2h"
        "&bookmakers=draftkings"
        "&commenceTimeFrom=2025-11-06"
        "&commenceTimeTo=2025-11-07"
    )
    
    try:
        print("Fetching Raiders @ Broncos...")
        time.sleep(5)
        response = requests.get(url, timeout=15)
        print(f"BULK STATUS: {response.status_code}")
        
        if response.status_code != 200:
            print("Rate limited — wait 30 seconds")
            return []
            
        data = response.json()
        print(f"FOUND {len(data)} game(s)")
        
        if data:
            event = data[0]
            return [{
                "id": event["id"],
                "home": event["home_team"],
                "away": event["away_team"],
                "commence_time": "2025-11-06"
            }]
        return []
    except Exception as e:
        print(f"Error: {e}")
        return []

def get_player_props(event_id):
    if not event_id:
        return []
        
    url = f"https://api.the-odds-api.com/v4/sports/americanfootball_nfl/events/{event_id}/odds"
    params = {
        "apiKey": ODDS_API_KEY,
        "regions": "us",
        "markets": "player_pass_yds,player_rush_yds,player_rec_yds",
        "oddsFormat": "american",
        "bookmakers": "draftkings,fanduel"
    }
    
    try:
        time.sleep(2)
        response = requests.get(url, params=params, timeout=15)
        print(f"PROPS STATUS: {response.status_code}")
        if response.status_code != 200:
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
        print(f"REAL PROPS: {len(props)}")
        return props[:10]
    except Exception as e:
        print(f"Error: {e}")
        return []