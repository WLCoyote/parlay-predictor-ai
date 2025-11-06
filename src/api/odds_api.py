import requests
from src.utils.config import ODDS_API_KEY

def get_player_props(game_key):
    """
    Fetch player prop odds (Over only) for a specific NFL game using The Odds API.
    Returns list of dicts: player, prop, odds, book.
    """
    sport = "americanfootball_nfl"
    markets = "player_pass_yds,player_rush_yds,player_rec_yds,player_pass_tds,player_rush_tds,player_receptions"
    
    url = f"https://api.the-odds-api.com/v4/sports/{sport}/events/{game_key}/odds"
    
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
        response.raise_for_status()
        data = response.json()

        props = []
        seen = set()  # Avoid duplicates

        for market in data.get("markets", []):
            bookmaker = market["key"].split("_")[-1].title()  # Clean name
            if bookmaker not in ["Draftkings", "Fanduel", "Betmgm"]:
                continue

            for outcome in market.get("outcomes", []):
                if outcome.get("name", "").lower().startswith("over"):
                    player = outcome.get("description", "Unknown Player")
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
                        "book": bookmaker
                    })

        # Sort by odds (best value first), limit to 8
        props.sort(key=lambda x: x["odds"], reverse=True)
        return props[:8]

    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            print(f"Odds API: No odds found for GameKey {game_key}")
        elif response.status_code == 401:
            print("Odds API: Invalid API key")
        else:
            print(f"Odds API HTTP Error: {e}")
        return []
    except requests.exceptions.RequestException as e:
        print(f"Odds API Request Failed: {e}")
        return []
    except Exception as e:
        print(f"Odds API Unexpected Error: {e}")
        return []