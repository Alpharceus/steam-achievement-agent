import requests
from ai_agent.prompt_templates import ACHIEVEMENT_RANK_PROMPT

def build_achievements_block(achievements, weights):
    lines = []
    for ach in achievements:
        line = (
            f"- Name: {ach['name']}\n"
            f"  Description: {ach.get('description', '')}\n"
            f"  Rarity: {ach.get('rarity', 'N/A')}\n"
            f"  Weight: {weights.get(ach['apiname'], 1.0)}\n"
        )
        lines.append(line)
    return "\n".join(lines)

def rank_achievements_with_llama(game_name, achievements, weights, model="llama3"):
    achievements_block = build_achievements_block(achievements, weights)
    prompt = ACHIEVEMENT_RANK_PROMPT.format(game_name=game_name, achievements_block=achievements_block)
    
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False  # Set to True later for streaming
        }
    )
    if response.ok:
        return response.json()["response"]
    else:
        raise RuntimeError(f"Ollama LLM API Error: {response.status_code} {response.text}")
