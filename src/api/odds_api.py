import requests
from src.utils.config import ODDS_API_KEY

def get_player_props(game_key):
    """
    Fetch player props using The Odds API.
    Converts SportsDataIO GameKey to Odds API event ID.
    """
    # Convert GameKey like '202511010' → '20251101-lv-den'
    try:
        # Extract date (first 8 digits)
        date_str = game_key[:8]  # e.g., '20251101'
        # We need team abbreviations from SportsDataIO response
        # But we don't have them here — so we need to pass them in
        # We'll fix this in app.py by passing teams
        pass
    except:
        print("Invalid GameKey format")
        return []

    # TEMP FIX: Use a known live game ID for testing
    # REPLACE WITH DYNAMIC LATER
    test_event_id = "20251110-den-lv"  # Example: DEN vs LV on Nov 10
    return _fetch_props_for_event(test_event_id)


def _fetch_props_for_event(event_id):
    """Internal: Fetch props for a valid Odds API event ID"""
    sport = "americanfootball_nfl"
    markets = "player_pass_yds,player_rush_yds,player_rec_yds,player_pass_tds,player_rush_tds,player_receptions"
    
    url = f"https://api.the-odds-api.com/v4/sports/{sport}/events/{event_id}/odds"
    
    params = {
        "apiKey": ODDS_API_KEY,
        "regions": "us",
        "markets": markets,
        "oddsFormat": "american",
        "bookmakers": "draftkings,fanduel,betmgm",
        "dateFormat": "iso"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 404:
            print(f"Odds API: No odds for event {event_id}")
            return []
        response.raise_for_status()
        data = response.json()

        props = []
        seen = set()

        for market in data.get("markets", []):
            book = market["key"].split("_")[-1].title()
            if book not in ["Draftkings", "Fanduel", "Betmgm"]:
                continue

            for outcome in market.get("outcomes", []):
                name = outcome.get("name", "")
                if "Over" not in name:
                    continue

                player = outcome.get("description", "Unknown")
                point = outcome.get("point", "")
                odds = outcome["price"]
                key = (player, point)

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
        return props[:8]

    except requests.exceptions.HTTPError as e:
        print(f"Odds API HTTP {response.status_code}: {e}")
        return []
    except Exception as e:
        print(f"Odds API Error: {e}")
        return []