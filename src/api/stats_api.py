# src/api/stats_api.py
import requests
import json
import os
from src.utils.config import SPORTSDATAIO_KEY

BASE_URL = "https://api.sportsdata.io/v3/nfl"
HISTORICAL_CACHE = "historical_data.json"

def get_upcoming_games():
    """Fetch Week 10 Sunday games (Nov 9, 2025)"""
    url = f"{BASE_URL}/scores/json/Schedules/2025REG"
    headers = {"Ocp-Apim-Subscription-Key": SPORTSDATAIO_KEY}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        games = response.json()
        week10_sunday = [
            g for g in games 
            if g.get("Week") == 10 
            and str(g.get("DateTime") or "").startswith("2025-11-09")
            and g.get("Status") == "Scheduled"
        ]
        print(f"Found {len(week10_sunday)} Week 10 Sunday games")
        return week10_sunday
    except Exception as e:
        print(f"Stats API Error: {e}")
        return []

def get_player_props(game_key):
    """Fetch REAL player projections for future games (as props)"""
    if not game_key:
        return []
    
    url = f"{BASE_URL}/projections/json/PlayerProps/{game_key}"
    headers = {"Ocp-Apim-Subscription-Key": SPORTSDATAIO_KEY}
    
    try:
        response = requests.get(url, headers=headers)
        print(f"PROPS STATUS: {response.status_code} for GameKey {game_key}")
        if response.status_code != 200:
            return []
        data = response.json()
        props = []
        for player in data:
            if player.get("ProjectedPassingYards"):
                props.append({
                    "player": player["Name"],
                    "prop": f"Over {player['ProjectedPassingYards']} passing yds",
                    "odds": -110,
                    "book": "DraftKings"
                })
            if player.get("ProjectedRushingYards"):
                props.append({
                    "player": player["Name"],
                    "prop": f"Over {player['ProjectedRushingYards']} rushing yds",
                    "odds": -115,
                    "book": "DraftKings"
                })
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

def load_historical_data():
    """Load cached historical stats"""
    if os.path.exists(HISTORICAL_CACHE):
        with open(HISTORICAL_CACHE, 'r') as f:
            data = json.load(f)
        print(f"Loaded {len(data)} historical players from cache")
        return data[:10]
    return []

def save_historical_data():
    """Pull and cache historical stats (run once)"""
    url = f"{BASE_URL}/stats/json/PlayerSeasonStats/2024"
    headers = {"Ocp-Apim-Subscription-Key": SPORTSDATAIO_KEY}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        stats = []
        for player in data:
            games = player.get("Games", 1)
            stats.append({
                "player": player.get("Name"),
                "passing_yards_avg": player.get("PassingYards", 0) / games,
                "rushing_yards_avg": player.get("RushingYards", 0) / games,
                "receiving_yards_avg": player.get("ReceivingYards", 0) / games,
            })
        with open(HISTORICAL_CACHE, 'w') as f:
            json.dump(stats, f)
        print(f"Saved {len(stats)} historical players to cache")
        return stats[:10]
    except Exception as e:
        print(f"Historical Error: {e}")
        return []