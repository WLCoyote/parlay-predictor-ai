# src/api/stats_api.py
import requests
from src.utils.config import SPORTSDATAIO_KEY

BASE_URL = "https://api.sportsdata.io/v3/nfl"

def get_upcoming_games():
    """Fetch upcoming NFL games from current week"""
    url = f"{BASE_URL}/scores/json/Schedules/2025REG"
    headers = {"Ocp-Apim-Subscription-Key": SPORTSDATAIO_KEY}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        games = response.json()
        upcoming = [g for g in games if g["Status"] == "Scheduled"]
        return upcoming[:1]  # TNF only
    except Exception as e:
        print(f"Stats API Error: {e}")
        return []

def get_player_props(game_key):
    """Fetch REAL prop odds from SportsDataIO"""
    if not game_key:
        return []
    
    url = f"{BASE_URL}/odds/json/GameProps/{game_key}"
    headers = {"Ocp-Apim-Subscription-Key": SPORTSDATAIO_KEY}
    
    try:
        response = requests.get(url, headers=headers)
        print(f"PROPS STATUS: {response.status_code}")
        if response.status_code != 200:
            return []
        data = response.json()
        props = []
        for prop in data:
            player = prop.get("PlayerName")
            prop_type = prop.get("PropType")  # e.g., "PassingYards"
            line = prop.get("OverUnder")  # the line
            over_odds = prop.get("OverUnderOdds")
            book = "DraftKings"  # Default for MVP
            if player and line and over_odds:
                prop_text = f"{prop_type} Over {line}"
                props.append({
                    "player": player,
                    "prop": prop_text,
                    "odds": over_odds,
                    "book": book
                })
        print(f"REAL PROP ODDS FOUND: {len(props)}")
        return props[:10]
    except Exception as e:
        print(f"Props Error: {e}")
        return []