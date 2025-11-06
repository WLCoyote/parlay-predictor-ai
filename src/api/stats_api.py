import requests
from src.utils.config import SPORTSDATAIO_KEY

BASE_URL = "https://api.sportsdata.io/v3/nfl"

def get_upcoming_games():
    """Fetch next 3 NFL games"""
    url = f"{BASE_URL}/scores/json/Games/2025"
    headers = {"Ocp-Apim-Subscription-Key": SPORTSDATAIO_KEY}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        games = response.json()
        return [g for g in games if g["Status"] == "Scheduled"][:3]
    except Exception as e:
        print(f"Stats API Error: {e}")
        return []