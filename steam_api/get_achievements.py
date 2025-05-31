import requests
from config import STEAM_API_KEY, STEAM_ID

def get_achievements(app_id):
    """
    Fetches achievements for a given game (by app_id) for the user.
    Returns a list of achievement dicts, or an empty list if not available.
    """
    url = "https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v1/"
    params = {
        "key": STEAM_API_KEY,
        "steamid": STEAM_ID,
        "appid": app_id
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if "playerstats" in data and "achievements" in data["playerstats"]:
            return data["playerstats"]["achievements"]
        else:
            print(f"No achievements data found for app_id {app_id}")
            return []
    except Exception as e:
        print(f"Error fetching achievements for app_id {app_id}: {e}")
        return []

def get_achievement_schema(app_id):
    """
    Gets the schema for a game's achievements (names, descriptions).
    Returns a dict of achievement data keyed by 'apiname'.
    """
    url = "https://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v2/"
    params = {
        "key": STEAM_API_KEY,
        "appid": app_id
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        achievements = {}
        for ach in data.get("game", {}).get("availableGameStats", {}).get("achievements", []):
            achievements[ach["name"]] = {
                "displayName": ach.get("displayName", ach["name"]),
                "description": ach.get("description", ""),
                "hidden": ach.get("hidden", 0)
            }
        return achievements  # dict keyed by 'apiname'
    except Exception as e:
        print(f"Error fetching schema for app_id {app_id}: {e}")
        return {}

def enrich_achievements_with_schema(player_achievements, achievement_schema):
    """
    Merge player achievement info with schema (for names, descriptions).
    """
    enriched = []
    for ach in player_achievements:
        schema = achievement_schema.get(ach['apiname'], {})
        enriched.append({
            "apiname": ach['apiname'],
            "achieved": ach['achieved'],
            "unlocktime": ach.get("unlocktime", 0),
            "name": schema.get("displayName", ach['apiname']),
            "description": schema.get("description", ""),
            "hidden": schema.get("hidden", 0)
        })
    return enriched
