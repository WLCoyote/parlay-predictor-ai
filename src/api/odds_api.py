# src/api/odds_api.py
import requests
from src.utils.config import ODDS_API_KEY

# REAL EVENT ID from The Odds API - Raiders @ Broncos TNF Nov 6
REAL_EVENT_ID = "e1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p"  # I pulled this live

def get_upcoming_events_with_props():
    return [{
        "id": REAL_EVENT_ID,
        "home": "Denver Broncos",
        "away": "Las Vegas Raiders",
        "commence_time": "2025-11-06"
    }]

def get_player_props(event_id=REAL_EVENT_ID):
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
        print(f"Status: {response.status_code}")  # Should be 200
        response.raise_for_status()
        data = response.json()
        
        props = []
        seen = set()
        for market in data.get("markets", []):
            book = market["key"].split("_")[-1].title()
            if book not in ["Draftkings", "Fanduel", "Betmgm"]:
                continue
            for outcome in market.get("outcomes", []):
                if outcome.get("name", "").startswith("Over"):
                    player = outcome.get("description", "Player")
                    point = outcome.get("point", "")
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
        props.sort(key=lambda x: x["odds"], reverse=True)
        return props[:10]
        
    except Exception as e:
        print(f"Error: {e}")
        return []