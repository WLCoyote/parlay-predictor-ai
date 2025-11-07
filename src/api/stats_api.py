# src/api/stats_api.py
import requests
from src.utils.config import SPORTSDATAIO_KEY

BASE_URL = "https://api.sportsdata.io/v3/nfl"

def get_upcoming_games(week=10):
    """Fetch Week 10 games (Thu-Sun-Mon, Nov 6-10, 2025)"""
    url = f"{BASE_URL}/scores/json/Schedules/2025REG"
    headers = {"Ocp-Apim-Subscription-Key": SPORTSDATAIO_KEY}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        games = response.json()
        # Filter for Week 10, Nov 6-10, 2025, scheduled
        week10_games = [
            g for g in games 
            if g.get("Week") == week 
            and g.get("DateTime", "").startswith(("2025-11-06", "2025-11-09", "2025-11-10"))
            and g.get("Status") == "Scheduled"
        ]
        print(f"Found {len(week10_games)} Week 10 games (Thu-Sun-Mon)")
        return week10_games
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
            # Passing
            if player.get("ProjectedPassingYards"):
                props.append({
                    "player": player["Name"],
                    "prop": f"Over {player['ProjectedPassingYards']} passing yds",
                    "odds": -110,  # Use real odds from /odds when closer; mock for MVP
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

def get_historical_player_stats(season=2024):
    """Pull historical player stats for ML training from past season"""
    url = f"{BASE_URL}/stats/json/PlayerSeasonStats/{season}"
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
                "hit_rate_over": 0.52  # Calculate from historical hits in Day 2
            })
        print(f"Historical stats pulled: {len(stats)} players")
        return stats[:10]
    except Exception as e:
        print(f"Historical Error: {e}")
        return []

def get_live_player_props(game_key):
    """Pull live/in-game props for ongoing games"""
    if not game_key:
        return []
    
    url = f"{BASE_URL}/scores/json/LivePlayerProps/{game_key}"
    headers = {"Ocp-Apim-Subscription-Key": SPORTSDATAIO_KEY}
    try:
        response = requests.get(url, headers=headers)
        print(f"LIVE PROPS STATUS: {response.status_code}")
        if response.status_code != 200:
            return []
        data = response.json()
        props = []
        for prop in data:
            player = prop.get("PlayerName")
            prop_type = prop.get("PropType")
            line = prop.get("LiveOverUnder")
            odds = prop.get("LiveOverOdds")
            book = "DraftKings"
            if player and line and odds:
                prop_text = f"{prop_type} Over {line} (LIVE)"
                props.append({
                    "player": player,
                    "prop": prop_text,
                    "odds": odds,
                    "book": book
                })
        return props[:10]
    except Exception as e:
        print(f"Live Props Error: {e}")
        return []