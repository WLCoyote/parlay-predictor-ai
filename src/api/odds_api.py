import requests
from src.utils.config import ODDS_API_KEY

def get_upcoming_events_with_props():
    """Return the Raiders @ Broncos matchup"""
    return [{
        "id": "sr:match:51622645",  # Real Odds API ID for LV @ DEN, Nov 6
        "home": "Denver Broncos",
        "away": "Las Vegas Raiders",
        "commence_time": "2025-11-06"
    }]

def get_player_props(event_id="sr:match:51622645"):
    """Fetch player props for Raiders @ Broncos (real data)"""
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
        print(f"Props Response for {event_id}: {response.status_code}")  # Debug
        if response.status_code == 404:
            print("No props yet — check back closer to Nov 6")
            return []
        response.raise_for_status()
        data = response.json()
        print(f"Markets returned: {len(data.get('markets', []))}")  # Debug
        
        props = []
        seen = set()
        for market in data.get("markets", []):
            book = market["key"].split("_")[-1].title()
            if book not in ["Draftkings", "Fanduel", "Betmgm"]:
                continue
            for outcome in market.get("outcomes", []):
                if "Over" not in outcome.get("name", ""):
                    continue
                player = outcome.get("description", "Unknown")
                point = outcome.get("point", "")
                odds = outcome["price"]
                key = (player, point, book)
                if key in seen:
                    continue
                seen.add(key)
                props.append({
                    "player": player,
                    "prop": f"Over {point}",
                    "odds": odds,
                    "book": book
                })
        print(f"Props found: {len(props)}")  # Debug
        props.sort(key=lambda x: x["odds"], reverse=True)
        return props[:10]
    
    except Exception as e:
        print(f"Odds API Props Error: {e}")
        return []