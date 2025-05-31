ACHIEVEMENT_RANK_PROMPT = """
You are an expert gamer assistant. Here are Steam achievements from the game '{game_name}'.
Each achievement has a name, description, global rarity, and a custom user priority weight (from 0.1 to 2.0).
Rank these achievements from highest to lowest priority for the user to pursue next, explaining your reasoning briefly.

Achievements:
{achievements_block}

Format your response as a numbered list, each item including the achievement name and a short rationale.
"""
