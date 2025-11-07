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
    """Fetch REAL player props from SportsDataIO"""
    if not game_key:
        return []
    
    url = f"{BASE_URL}/projections/json/PlayerProps/{game_key}"
    headers = {"Ocp-Apim-Subscription-Key": SPORTSDATAIO_KEY}
    
    try:
        response = requests.get(url, headers=headers)
        print(f"PROPS STATUS: {response.status_code}")
        if response.status_code != 200:
            return []
        data = response.json()
        props = []
        for player in data:
            # Passing
            if player.get("ProjectedPassingYards"):
                props.append({
                    "player": player["Name"],
                    "prop": f"Over {player['ProjectedPassingYards']} passing yds",
                    "odds": -110,
                    "book": "DraftKings"
                })
            # Rushing
            if player.get("ProjectedRushingYards"):
                props.append({
                    "player": player["Name"],
                    "prop": f"Over {player['ProjectedRushingYards']} rushing yds",
                    "odds": -115,
                    "book": "DraftKings"
                })
            # Receiving
            if player.get("ProjectedReceivingYards"):
                props.append({
                    "player": player["Name"],
                    "prop": f"Over {player['ProjectedReceivingYards']} receiving yds",
                    "odds": +105,
                    "book": "DraftKings"
                })
        print(f"REAL PROPS FOUND: {len(props)}")
        return props[:10]
    except Exception as e:
        print(f"Props Error: {e}")
        return []