# src/api/odds_api.py
import requests
from src.utils.config import ODDS_API_KEY

def get_upcoming_events_with_props():
    """Fetch upcoming NFL events and filter for Raiders @ Broncos"""
    sport = "americanfootball_nfl"
    url = f"https://api.the-odds-api.com/v4/sports/{sport}/events"
    params = {
        "apiKey": ODDS_API_KEY,
        "daysFrom": "3",  # Next 3 days to catch TNF
        "dateFormat": "iso"
    }
    
    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        print(f"Events fetched: {len(data)}")  # Debug
        
        # Filter for Raiders @ Broncos
        for event in data:
            away = event.get("away_team", "").lower()
            home = event.get("home_team", "").lower()
            if "raiders" in away and "broncos" in home:
                return [{
                    "id": event["id"],  # Real hex ID
                    "home": event["home_team"],
                    "away": event["away_team"],
                    "commence_time": event["commence_time"][:10]
                }]
        print("Raiders @ Broncos not found in next 3 days — check date")  # Debug
        return []
    
    except Exception as e:
        print(f"Events Error: {e}")
        return []

def get_player_props(event_id):
    """Fetch player props for the event ID"""
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
        print(f"Props Status: {response.status_code}")  # Debug
        if response.status_code == 404:
            print("No props yet — too early")
            return []
        response.raise_for_status()
        data = response.json()
        print(f"Markets: {len(data.get('markets', []))}")  # Debug
        
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
        print(f"Props: {len(props)}")  # Debug
        props.sort(key=lambda x: x["odds"], reverse=True)
        return props[:10]
    
    except Exception as e:
        print(f"Props Error: {e}")
        return []