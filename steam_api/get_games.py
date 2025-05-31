import requests
from config import STEAM_API_KEY, STEAM_ID

def get_owned_games():
    """
    Fetches the list of games owned by the user.
    Returns a list of dicts, each with info about a game.
    """
    url = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/"
    params = {
        "key": STEAM_API_KEY,
        "steamid": STEAM_ID,
        "include_appinfo": True,
        "include_played_free_games": True
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        games = data["response"].get("games", [])
        return games
    except Exception as e:
        print(f"Error fetching owned games: {e}")
        return []
