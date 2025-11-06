# src/api/odds_api.py
import requests
from datetime import datetime, timedelta
from src.utils.config import ODDS_API_KEY

def get_upcoming_events_with_props():
    sport = "americanfootball_nfl"
    markets = "h2h"  # Safe market to get event IDs
    
    # Correct date format: YYYY-MM-DD (no time, no Z)
    today = datetime.utcnow().strftime("%Y-%m-%d")
    in_3_days = (datetime.utcnow() + timedelta(days=3)).strftime("%Y-%m-%d")
    
    url = f"https://api.the-odds-api.com/v4/sports/{sport}/odds"
    params = {
        "apiKey": ODDS_API_KEY,
        "regions": "us",
        "markets": markets,
        "oddsFormat": "american",
        "bookmakers": "draftkings,fanduel,betmgm",
        "commenceTimeFrom": today,
        "commenceTimeTo": in_3_days
    }
    
    try:
        response = requests.get(url, params=params, timeout=15)
        print(f"Bulk Status: {response.status_code}")
        if response.status_code != 200:
            print("API rejected date format — using fallback")
            return []
        data = response.json()
        print(f"Found {len(data)} games with odds")
        
        if data:
            event = data[0]
            return [{
                "id": event["id"],
                "home": event["home_team"],
                "away": event["away_team"],
                "commence_time": event["commence_time"][:10]
            }]
        return []
    except Exception as e:
        print(f"Error: {e}")
        return []

def get_player_props(event_id):
    if not event_id:
        return []
        
    sport = "americanfootball_nfl"
    markets = "player_pass_yds,player_rush_yds,player_rec_yds,player_pass_tds,player_rush_tds,player_receptions"
    url = f"https://api.the-odds-api.com/v4/sports/{sport}/events/{event_id}/odds"
    
    params = {
        "apiKey": ODDS_API_KEY,
        "regions": "us",
        "markets": markets,
        "oddsFormat": "american",
        "bookmakers": "draftkings,fanduel,betmgm"
    }
    
    try:
        response = requests.get(url, params=params, timeout=15)
        print(f"Props Status: {response.status_code}")
        if response.status_code != 200:
            print("Props not live yet — normal for early games")
            return []
        data = response.json()
        props = []
        seen = set()
        for market in data.get("markets", []):
            book = market["key"].split("_")[-1].title()
            for outcome in market.get("outcomes", []):
                name = outcome.get("name", "")
                if name.startswith("Over"):
                    player = outcome.get("description", "Player")
                    point = outcome.get("point")
                    odds = outcome["price"]
                    key = (player, point)
                    if key in seen:
                        continue
                    seen.add(key)
                    props.append({
                        "player": player,
                        "prop": f"Over {point}",
                        "odds": odds,
                        "book": book
                    })
        print(f"REAL PROPS FOUND: {len(props)}")
        props.sort(key=lambda x: x["odds"], reverse=True)
        return props[:10]
    except Exception as e:
        print(f"Props Error: {e}")
        return []