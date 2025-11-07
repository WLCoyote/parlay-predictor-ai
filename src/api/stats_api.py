# src/api/stats_api.py
import requests
from src.utils.config import SPORTSDATAIO_KEY

BASE_URL = "https://api.sportsdata.io/v3/nfl"

def get_current_week():
    """Get the current/active week from Timeframes"""
    url = f"{BASE_URL}/scores/json/Timeframes"
    headers = {"Ocp-Apim-Subscription-Key": SPORTSDATAIO_KEY}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        timeframes = response.json()
        # Find current timeframe (Week 10 in 2025)
        current = next((tf for tf in timeframes if tf["HasEnded"] == False and tf["Week"] == 10), None)
        if current:
            print(f"Current Week: {current['Week']}")
            return current["Week"]
        return 10  # Default to Week 10
    except Exception as e:
        print(f"Timeframes Error: {e}")
        return 10

def get_upcoming_games(week=10):
    """Fetch Week 10 Sunday games (Nov 9, 2025)"""
    url = f"{BASE_URL}/scores/json/Schedules/2025REG"
    headers = {"Ocp-Apim-Subscription-Key": SPORTSDATAIO_KEY}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        games = response.json()
        # Filter for Week 10, Sunday (Nov 9, 2025), scheduled
        week10_sunday = [
            g for g in games 
            if g.get("Week") == week 
            and (g.get("DateTime") or "").startswith("2025-11-09")
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
                "hit_rate_over": 0.52  # Mock for MVP; calculate from historical hits
            })
        print(f"Historical stats pulled: {len(stats)} players")
        return stats[:10]
    except Exception as e:
        print(f"Historical Error: {e}")
        return []