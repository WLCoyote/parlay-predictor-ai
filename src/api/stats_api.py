# src/api/stats_api.py
import requests
from src.utils.config import SPORTSDATAIO_KEY

BASE_URL = "https://api.sportsdata.io/v3/nfl"

def get_upcoming_games():
    """Fetch Week 10 Sunday games (Nov 9, 2025)"""
    url = f"{BASE_URL}/scores/json/Schedules/2025REG"
    headers = {"Ocp-Apim-Subscription-Key": SPORTSDATAIO_KEY}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        games = response.json()
        # Fixed filter: Week 10, Sunday (Nov 9, 2025), scheduled
        week10_sunday = [
            g for g in games 
            if g.get("Week") == 10 
            and g.get("DateTime", "").startswith("2025-11-09")
            and g.get("Status") == "Scheduled"
        ]
        print(f"Found {len(week10_sunday)} Week 10 Sunday games")
        return week10_sunday
    except Exception as e:
        print(f"Stats API Error: {e}")
        return []

def get_player_props(game_key):
    """Fetch REAL player prop odds from SportsDataIO"""
    if not game_key:
        return []
    
    url = f"{BASE_URL}/odds/json/PlayerPropOdds/{game_key}"
    headers = {"Ocp-Apim-Subscription-Key": SPORTSDATAIO_KEY}
    
    try:
        response = requests.get(url, headers=headers)
        print(f"PROPS STATUS: {response.status_code} for GameKey {game_key}")
        if response.status_code != 200:
            return []
        data = response.json()
        props = []
        for prop in data:
            player = prop.get("PlayerName")
            prop_type = prop.get("PropType")
            line = prop.get("OverUnder")
            over_odds = prop.get("OverUnderOdds")
            book = prop.get("Sportsbook", "DraftKings")
            if player and line and over_odds:
                prop_text = f"{prop_type} Over {line}"
                props.append({
                    "player": player,
                    "prop": prop_text,
                    "odds": over_odds,
                    "book": book
                })
        print(f"REAL PROPS FOUND: {len(props)}")
        return props[:10]
    except Exception as e:
        print(f"Props Error: {e}")
        return []