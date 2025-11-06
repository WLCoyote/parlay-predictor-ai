import requests
from datetime import datetime, timedelta
from src.utils.config import ODDS_API_KEY

def get_upcoming_events_with_props():
    """Fetch upcoming NFL games with player props (within next 7 days)"""
    sport = "americanfootball_nfl"
    markets = "player_pass_yds,player_rush_yds,player_rec_yds,player_pass_tds,player_rush_tds,player_receptions"
    
    # Time window: now to +7 days
    now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    future = (datetime.utcnow() + timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%SZ")
    
    url = f"https://api.the-odds-api.com/v4/sports/{sport}/odds"
    params = {
        "apiKey": ODDS_API_KEY,
        "regions": "us",
        "markets": markets,
        "oddsFormat": "american",
        "bookmakers": "draftkings,fanduel,betmgm",
        "commenceTimeFrom": now,
        "commenceTimeTo": future,
        "dateFormat": "iso"
    }
    
    try:
        response = requests.get(url, params=params, timeout=15)
        if response.status_code == 422:
            print("422: Missing time params — using fallback")
            return []
        response.raise_for_status()
        data = response.json()

        events = []
        for event in data:
            if not event.get("bookmakers"):
                continue
            events.append({
                "id": event["id"],
                "home": event["home_team"],
                "away": event["away_team"],
                "commence_time": event["commence_time"][:10]
            })
        return events[:3]
    
    except Exception as e:
        print(f"Odds API Events Error: {e}")
        return []

def get_player_props(event_id):
    """Fetch player props for a real event ID"""
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
        response.raise_for_status()
        data = response.json()
        
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
        props.sort(key=lambda x: x["odds"], reverse=True)
        return props[:10]
    
    except Exception as e:
        print(f"Odds API Props Error: {e}")
        return []