# src/api/odds_api.py
import requests
import time
from src.utils.config import ODDS_API_KEY
from datetime import datetime, timedelta

def get_upcoming_events_with_props():
    sport = "americanfootball_nfl"
    url = f"https://api.the-odds-api.com/v4/sports/{sport}/odds"
    
    # FULL ISO FORMAT (required to avoid 422)
    now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    future = (datetime.utcnow() + timedelta(days=3)).strftime("%Y-%m-%dT%H:%M:%SZ")
    
    params = {
        "apiKey": ODDS_API_KEY,
        "regions": "us",
        "markets": "h2h",
        "oddsFormat": "american",
        "bookmakers": "draftkings,fanduel,betmgm",
        "commenceTimeFrom": now,
        "commenceTimeTo": future
    }
    
    try:
        time.sleep(5)  # Avoid rate limit
        response = requests.get(url, params=params, timeout=15)
        print(f"BULK STATUS: {response.status_code} | Remaining: {response.headers.get('x-requests-remaining', 'Unknown')}")
        response.raise_for_status()
        data = response.json()
        print(f"Found {len(data)} games")
        
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
        print(f"Bulk Error: {e}")
        return []

def get_player_props(event_id):
    if not event_id:
        return []
    
    sport = "americanfootball_nfl"
    url = f"https://api.the-odds-api.com/v4/sports/{sport}/events/{event_id}/odds"
    params = {
        "apiKey": ODDS_API_KEY,
        "regions": "us",
        "markets": "player_pass_yds,player_rush_yds,player_rec_yds,player_pass_tds,player_rush_tds,player_receptions",
        "oddsFormat": "american",
        "bookmakers": "draftkings,fanduel,betmgm"
    }
    
    try:
        time.sleep(2)
        response = requests.get(url, params=params, timeout=15)
        print(f"PROPS STATUS: {response.status_code}")
        if response.status_code != 200:
            print("Props not live yet — normal for early games")
            return []
        response.raise_for_status()
        data = response.json()
        print(f"Markets: {len(data.get('markets', []))}")
        
        props = []
        seen = set()
        for market in data.get("markets", []):
            book = market["key"].split("_")[-1].title()
            for outcome in market.get("outcomes", []):
                if outcome.get("name", "").startswith("Over"):
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
        print(f"Real props found: {len(props)}")
        props.sort(key=lambda x: x["odds"], reverse=True)
        return props[:10]
    except Exception as e:
        print(f"Props Error: {e}")
        return []