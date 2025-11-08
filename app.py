# app.py
import streamlit as st
from src.api.stats_api import get_upcoming_games, get_player_props, load_historical_data, save_historical_data

st.set_page_config(page_title="Parlay Predictor AI", layout="wide")
st.title("PARLAY PREDICTOR AI")
st.caption("Week 10 Sunday Games • Nov 9, 2025")

st.warning("For entertainment only. 18+. Gamble responsibly.")

# Load historical on startup
historical_stats = load_historical_data()

if st.button("GENERATE LIVE PARLAYS", type="primary", use_container_width=True):
    with st.spinner("Pulling Week 10 Sunday props..."):
        games = get_upcoming_games()
        if not games:
            st.error("No Week 10 Sunday games found — check SportsDataIO key")
        else:
            for game in games:
                st.subheader(f"**{game['AwayTeam']} @ {game['HomeTeam']}**")
                st.write(f"Kickoff: {game['DateTime']} (5:15 PM PT / 8:15 PM ET)")
                st.write(f"Line: {game.get('PointSpread', 'TBD')} | O/U {game.get('OverUnder', 'TBD')}")
                
                props = get_player_props(game["GameKey"])
                if props:
                    st.write("**Top 10 Player Props (PROJECTED ODDS)**")
                    for p in props:
                        st.write(f"• **{p['player']}** — {p['prop']} @ **{p['odds']}** ({p['book']})")
                else:
                    st.info("Props syncing — refresh in 30 min")

if st.button("REFRESH HISTORICAL DATA (ONCE PER SEASON)"):
    with st.spinner("Pulling 2024 historical stats..."):
        save_historical_data()

if historical_stats:
    st.subheader("Historical Player Stats (For ML Training)")
    for s in historical_stats:
        st.write(f"• **{s['player']}** — Avg Passing: {s['passing_yards_avg']:.0f}, Rushing: {s['rushing_yards_avg']:.0f}")