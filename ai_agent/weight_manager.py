import json
import os

WEIGHTS_PATH = "data/weights.json"

def load_weights():
    if not os.path.exists(WEIGHTS_PATH):
        return {}
    with open(WEIGHTS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_weights(weights):
    os.makedirs(os.path.dirname(WEIGHTS_PATH), exist_ok=True)
    with open(WEIGHTS_PATH, "w", encoding="utf-8") as f:
        json.dump(weights, f, indent=2)

def get_weight(game_id, ach_apiname, weights):
    # Returns the weight for an achievement, defaults to 1.0
    game_id = str(game_id)
    return weights.get(game_id, {}).get(ach_apiname, 1.0)

def set_weight(game_id, ach_apiname, value, weights):
    game_id = str(game_id)
    if game_id not in weights:
        weights[game_id] = {}
    weights[game_id][ach_apiname] = value
    save_weights(weights)
