import requests
from src.utils.config import ODDS_API_KEY

def get_player_props():
    """
    TEMP: Fetch props for a known live game (KC @ DEN, Week 10)
    Returns real player props with live odds.
    """
    # REAL EVENT ID: 2025-11-10, KC @ DEN
    event_id = "20251110-kc-den"
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
            print(f"No odds for {event_id} (too early?)")
            return []
        if response.status_code == 422:
            print(f"422: Invalid event ID: {event_id}")
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
        print(f"Odds API Error: {e}")
        return []