# app.py
import streamlit as st
from src.api.stats_api import get_upcoming_games
from src.api.odds_api import get_upcoming_events_with_props, get_player_props

st.set_page_config(page_title="Parlay Predictor AI", layout="centered")
st.title("Parlay Predictor AI")
st.caption("AI-powered value parlay builder • MVP v1.4")

st.warning("For entertainment only. 18+. Gamble responsibly.")

if st.button("Generate Parlay"):
    with st.spinner("Fetching live NFL data..."):
        # Use The Odds API for matchup + props (consistent ID)
        events = get_upcoming_events_with_props()
        if not events:
            st.error("No games with props yet. Check back closer to kickoff.")
        else:
            event = events[0]
            st.success(f"**Matchup**: {event['away']} @ {event['home']} (Starts {event['commence_time'][:10]})")
            props = get_player_props(event["id"])
            if props:
                st.subheader("Top Player Props (LIVE ODDS)")
                for p in props:
                    st.write(f"• **{p['player']}** — {p['prop']} @ **{p['odds']}** ({p['book']})")
            else:
                st.info("Props loading — game may be too far out.")