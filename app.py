# app.py
import streamlit as st
from src.api.stats_api import get_upcoming_games, get_player_props

st.set_page_config(page_title="Parlay Predictor AI", layout="centered")
st.title("PARLAY PREDICTOR AI")
st.caption("LIVE TNF Props • Raiders @ Broncos • Nov 6, 2025")

st.warning("For entertainment only. 18+. Gamble responsibly.")

if st.button("GENERATE LIVE PARLAY", type="primary", use_container_width=True):
    with st.spinner("Pulling real player props..."):
        games = get_upcoming_games()
        if not games:
            st.error("No games found — check SportsDataIO key")
        else:
            game = games[0]
            st.success("**Thursday Night Football**")
            st.write(f"**{game['AwayTeam']} @ {game['HomeTeam']}**")
            st.write("Kickoff: 6:15 PM ET • Prime Video")
            st.write("Early Line: DEN -9 | O/U 42.5")
            
            props = get_player_props(game["GameKey"])
            if props:
                st.subheader("TOP 10 PLAYER PROPS (LIVE ODDS)")
                for p in props:
                    st.write(f"• **{p['player']}** — {p['prop']} @ **{p['odds']}** ({p['book']})")
            else:
                st.info("Props syncing — refresh in 30 min")