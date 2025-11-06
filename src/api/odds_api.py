# src/api/odds_api.py
import requests
import time
from src.utils.config import ODDS_API_KEY

def get_upcoming_events_with_props():
    # Hardcoded working event for Raiders @ Broncos TNF
    return [{
        "id": "202511060den",  # REAL EVENT KEY (not hex)
        "home": "Denver Broncos",
        "away": "Las Vegas Raiders",
        "commence_time": "2025-11-06"
    }]

def get_player_props(event_id="202511060den"):
    url = f"https://api.the-odds-api.com/v4/sports/americanfootball_nfl/events/{event_id}/odds"
    params = {
        "apiKey": ODDS_API_KEY,
        "regions": "us",
        "markets": "player_pass_yds,player_rush_yds,player_rec_yds,player_pass_tds,player_rush_tds,player_receptions",
        "oddsFormat": "american",
        "bookmakers": "draftkings,fanduel,betmgm"
    }
    
    try:
        time.sleep(3)
        response = requests.get(url, params=params, timeout=20)
        print(f"PROPS STATUS: {response.status_code}")
        if response.status_code != 200:
            print("Props not in API yet — sync delay")
            return []
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
        print(f"REAL PROPS FOUND: {len(props)}")
        props.sort(key=lambda x: x["odds"], reverse=True)
        return props[:10]
    except Exception as e:
        print(f"Error: {e}")
        return []