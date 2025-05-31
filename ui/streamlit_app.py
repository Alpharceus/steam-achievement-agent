import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from steam_api.get_games import get_owned_games
from steam_api.get_achievements import (
    get_achievements, get_achievement_schema, enrich_achievements_with_schema
)
from steam_api.utils import get_unlocked_and_locked_achievements
from ai_agent.weight_manager import load_weights, set_weight
from ai_agent.llama_ranker import rank_achievements_with_llama

# --- Custom CSS for stylish background and sidebar ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(120deg, #232526, #414345 85%, #232526);
        min-height: 100vh;
    }
    section[data-testid="stSidebar"] {
        background: rgba(30, 32, 40, 0.8) !important;
        backdrop-filter: blur(5px);
    }
    .achievement-card {
        background: rgba(40, 44, 52, 0.7);
        padding: 1em;
        border-radius: 12px;
        margin-bottom: 0.75em;
        box-shadow: 0 1px 8px #0004;
    }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar Logo and Progress ---
st.sidebar.image("pictures/logo.png", width=48)

st.sidebar.title("Your Progress & AI Agent")

# --- Main Title ---
st.title("Steam Achievement Agent")

# --- Load Games ---
games = get_owned_games()
if not games:
    st.warning("No games found for this account!")
    st.stop()

game_options = {game['name']: game['appid'] for game in games}
selected_game = st.selectbox("Select a game:", list(game_options.keys()))

achievements = None  # So sidebar doesn't error before game selection

if selected_game:
    appid = game_options[selected_game]
    # Fetch and enrich achievements
    player_achievements = get_achievements(appid)
    achievement_schema = get_achievement_schema(appid)
    achievements = enrich_achievements_with_schema(player_achievements, achievement_schema)

    if not achievements:
        st.warning("No achievements found for this game!")
        st.stop()

    unlocked, locked = get_unlocked_and_locked_achievements(achievements)
    unlocked_count = len(unlocked)
    total = len(achievements)
    percent = unlocked_count / total * 100 if total else 0

    # --- Sidebar: Achievement Counter & Progress ---
    st.sidebar.markdown(f"### Achievements Unlocked")
    st.sidebar.markdown(f"**{unlocked_count} / {total}**  ({percent:.1f}%)")
    st.sidebar.progress(percent / 100)
    st.sidebar.markdown("---")
    st.sidebar.markdown("## AI Achievement Ranking")
    st.sidebar.markdown(
        "Get a ranked list of your locked achievements—personalized by your weights, rarity, and context. "
        "This only looks at your first 10 locked achievements for faster responses."
    )

    if st.sidebar.button("Ask AI to Rank My Locked Achievements"):
        st.sidebar.info("Calling Llama agent, please wait...")
        locked_subset = locked[:10] if len(locked) > 10 else locked
        ai_weights = load_weights().get(str(appid), {})
        with st.spinner("AI is thinking..."):
            response = rank_achievements_with_llama(selected_game, locked_subset, ai_weights)
        st.sidebar.markdown(f"### AI Suggestion:\n{response}")

    # --- Main Area ---
    mode = st.radio("Which achievements to view?", ("Locked (needed)", "Unlocked"))

    if mode == "Unlocked":
        st.subheader("Unlocked Achievements")
        if not unlocked:
            st.info("You haven't unlocked any achievements yet!")
        for ach in unlocked:
            st.markdown(
                f"<div class='achievement-card'>"
                f"✅ <b>{ach['name']}</b>: {ach.get('description', '')}"
                f"</div>",
                unsafe_allow_html=True
            )
    else:
        st.subheader("Locked Achievements")
        if not locked:
            st.success("You've unlocked all achievements! 🎉")
        else:
            weights = load_weights().get(str(appid), {})
            for ach in locked:
                weight = weights.get(ach['apiname'], 1.0)
                col1, col2, col3 = st.columns([3, 4, 2])
                with col1:
                    st.markdown(
                        f"<div class='achievement-card'><b>{ach['name']}</b></div>",
                        unsafe_allow_html=True
                    )
                with col2:
                    st.markdown(
                        f"<div class='achievement-card'>{ach.get('description', '')}</div>",
                        unsafe_allow_html=True
                    )
                with col3:
                    new_weight = st.slider(
                        f"Weight for {ach['name']}", 0.1, 2.0, float(weight), 0.1, key=ach['apiname']
                    )
                    if new_weight != weight:
                        set_weight(appid, ach['apiname'], new_weight, load_weights())

# Footer or About
st.markdown(
    "<br><hr style='border:1px solid #555;'><center><small>Built with ❤️ using Streamlit and Ollama • "
    "Not affiliated with Steam/Valve • Designed by Raman and ChatGPT</small></center>",
    unsafe_allow_html=True,
)
# --- End of Streamlit App ---