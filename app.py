import streamlit as st
from src.api.stats_api import get_upcoming_games
from src.api.odds_api import get_player_props

st.set_page_config(page_title="Parlay Predictor AI", layout="centered")
st.title("Parlay Predictor AI")
st.caption("AI-powered value parlay builder • MVP v1.0")

st.warning("For entertainment only. 18+. Gamble responsibly.")

if st.button("Generate Parlay"):
    with st.spinner("Fetching live data..."):
        games = get_upcoming_games()
        if not games:
            st.error("No upcoming games found. Check API keys.")
        else:
            game = games[0]  # First game
            st.success(f"Matchup: {game['AwayTeam']} @ {game['HomeTeam']}")
            
            props = get_player_props(game["GameKey"])
            if props:
                st.subheader("Top Value Props")
                for p in props:
                    st.write(f"**{p['player']}** — {p['prop']} @ **{p['odds']}** ({p['book']})")
            else:
                st.info("No player props available yet.")