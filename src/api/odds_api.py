import requests
from src.utils.config import ODDS_API_KEY

def get_player_props(game_key):
    """Fetch player prop odds for a game (e.g., rushing yards)"""
    sport = "americanfootball_nfl"
    markets = "player_rush_yds,player_pass_yds,player_rec_yds"
    url = f"https://api.the-odds-api.com/v4/sports/{sport}/events/{game_key}/odds"
    params = {
        "apiKey": ODDS_API_KEY,
        "regions": "us",
        "markets": markets,
        "oddsFormat": "american",
        "bookmakers": "draftkings,fanduel"
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        props = []
        for market in data.get("markets", []):
            for outcome in market["outcomes"]:
                if "Over" in outcome["name"]:
                    props.append({
                        "player": outcome["description"],
                        "prop": f"{outcome['name']} {outcome['point']}",
                        "odds": outcome["price"],
                        "book": market["bookmaker_title"]
                    })
        return props[:6]  # Top 6 props
    except Exception as e:
        print(f"Odds API Error: {e}")
        return []