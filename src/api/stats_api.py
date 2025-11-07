# src/api/stats_api.py
import requests
from src.utils.config import SPORTSDATAIO_KEY

BASE_URL = "https://api.sportsdata.io/v3/nfl"

def get_upcoming_games(week=11):  # Default to next week
    """Fetch upcoming NFL games for a week (e.g., Week 11 Sunday)"""
    url = f"{BASE_URL}/scores/json/Schedules/2024REG"
    headers = {"Ocp-Apim-Subscription-Key": SPORTSDATAIO_KEY}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        games = response.json()
        upcoming = [g for g in games if g.get("Week") == week and g.get("Status") == "Scheduled"]
        print(f"Found {len(upcoming)} Week {week} games")
        return upcoming
    except Exception as e:
        print(f"Stats API Error: {e}")
        return []

def get_player_props(game_key):
    """Fetch REAL player prop odds for a game"""
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

def get_historical_player_stats(season=2024):
    """Pull historical player stats for ML training (past seasons)"""
    url = f"{BASE_URL}/scores/json/PlayerSeasonStats/{season}"
    headers = {"Ocp-Apim-Subscription-Key": SPORTSDATAIO_KEY}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        stats = []
        for player in data:
            stats.append({
                "player": player.get("Name"),
                "passing_yards_avg": player.get("PassingYards") / player.get("Games", 1),
                "rushing_yards_avg": player.get("RushingYards") / player.get("Games", 1),
                "receiving_yards_avg": player.get("ReceivingYards") / player.get("Games", 1),
                "hit_rate_over": player.get("OverUnderHitRate", 0.5)  # Mock for MVP; use historical hits
            })
        print(f"Historical stats pulled: {len(stats)} players")
        return stats
    except Exception as e:
        print(f"Historical Error: {e}")
        return []