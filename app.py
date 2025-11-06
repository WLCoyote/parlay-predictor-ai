import streamlit as st
from src.api.odds_api import get_upcoming_events_with_props, get_player_props

st.set_page_config(page_title="Parlay Predictor AI", layout="centered")
st.title("Parlay Predictor AI")
st.caption("AI-powered value parlay builder • MVP v1.6")

st.warning("For entertainment only. 18+. Gamble responsibly.")

if st.button("Generate Parlay"):
    with st.spinner("Fetching Raiders @ Broncos props..."):
        events = get_upcoming_events_with_props()
        if not events:
            st.error("No games available.")
        else:
            event = events[0]
            st.success(f"**TNF Matchup**: {event['away']} @ {event['home']} (Nov 6, 2025)")
            props = get_player_props()
            if props:
                st.subheader("Top Player Props (LIVE ODDS)")
                for p in props:
                    st.write(f"• **{p['player']}** — {p['prop']} @ **{p['odds']}** ({p['book']})")
            else:
                st.info("Props not posted yet — check back Nov 5 PM. Early lines: DEN -9.")