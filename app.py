import streamlit as st
from src.api.stats_api import get_upcoming_games
from src.api.odds_api import get_player_props

st.set_page_config(page_title="Parlay Predictor AI", layout="centered")
st.title("Parlay Predictor AI")
st.caption("AI-powered value parlay builder • MVP v1.3")

st.warning("For entertainment only. 18+. Gamble responsibly.")

if st.button("Generate Parlay"):
    with st.spinner("Fetching live NFL data..."):
        games = get_upcoming_games()
        if not games:
            st.error("No schedule. Check SportsDataIO key.")
        else:
            game = games[0]
            st.success(f"**Next Game**: {game['AwayTeam']} @ {game['HomeTeam']} (Week {game['Week']})")

            props = get_player_props()  # TEMP: Hardcoded KC @ DEN
            if props:
                st.subheader("Top Player Props (LIVE ODDS)")
                for p in props:
                    st.write(f"• **{p['player']}** — {p['prop']} @ **{p['odds']}** ({p['book']})")
            else:
                st.info("No props yet — game too far out.")