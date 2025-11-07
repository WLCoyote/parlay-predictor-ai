# app.py
import streamlit as st
from src.api.stats_api import get_upcoming_games, get_player_props, get_historical_player_stats

st.set_page_config(page_title="Parlay Predictor AI", layout="wide")
st.title("PARLAY PREDICTOR AI")
st.caption("Week 11 Sunday Games • Nov 17, 2024")

st.warning("For entertainment only. 18+. Gamble responsibly.")

if st.button("GENERATE LIVE PARLAYS", type="primary", use_container_width=True):
    with st.spinner("Pulling Week 11 Sunday props..."):
        games = get_upcoming_games(week=11)
        if not games:
            st.error("No Week 11 Sunday games found — check SportsDataIO key")
        else:
            for game in games:
                st.subheader(f"**{game['AwayTeam']} @ {game['HomeTeam']}**")
                st.write(f"Kickoff: {game['DateTime']} (e.g., 1 PM ET for Ravens @ Browns)")
                st.write(f"Line: {game.get('PointSpread', 'TBD')} | O/U {game.get('OverUnder', 'TBD')}")
                
                props = get_player_props(game["GameKey"])
                if props:
                    st.write("**Top 10 Player Props (LIVE ODDS)**")
                    for p in props:
                        st.write(f"• **{p['player']}** — {p['prop']} @ **{p['odds']}** ({p['book']})")
                else:
                    st.info("Props syncing — refresh in 30 min")

if st.button("LOAD HISTORICAL DATA FOR ML"):
    with st.spinner("Pulling 2024 historical stats for training..."):
        stats = get_historical_player_stats(season=2024)
        if stats:
            st.subheader("Historical Player Stats (For ML Training)")
            for s in stats[:10]:
                st.write(f"• **{s['player']}** — Avg Passing: {s['passing_yards_avg']:.0f}, Hit Rate: {s['hit_rate_over']:.1%}")
        else:
            st.info("Historical data syncing — refresh in 1 min")