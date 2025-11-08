# app.py
import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo
from src.api.stats_api import get_upcoming_games, get_player_props, load_historical_data

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
                # Parse UTC time
                utc_time = datetime.fromisoformat(game["DateTime"].replace("Z", "+00:00"))
                pt_time = utc_time.astimezone(ZoneInfo("America/Los_Angeles"))
                et_time = utc_time.astimezone(ZoneInfo("America/New_York"))
                
                st.subheader(f"**{game['AwayTeam']} @ {game['HomeTeam']}**")
                st.write(f"Kickoff: {game['DateTime']} UTC → **{pt_time.strftime('%-I:%M %p PT')} / {et_time.strftime('%-I:%M %p ET')}**")
                st.write(f"Line: {game.get('PointSpread', 'TBD')} | O/U {game.get('OverUnder', 'TBD')}")
                
                props = get_player_props(game["GameKey"])
                if props:
                    st.write("**Top 10 Player Props (PROJECTED ODDS)**")
                    for p in props:
                        st.write(f"• **{p['player']}** — {p['prop']} @ **{p['odds']}** ({p['book']})")
                else:
                    st.info("Real odds appear 24-36 hours before kickoff — refresh tomorrow")

if historical_stats:
    st.subheader("Historical Player Stats (For ML Training)")
    for s in historical_stats:
        st.write(f"• **{s['player']}** — Avg Passing: {s['passing_yards_avg']:.0f}, Rushing: {s['rushing_yards_avg']:.0f}")