# app.py
import streamlit as st
from src.api.odds_api import get_upcoming_events_with_props, get_player_props

st.set_page_config(page_title="Parlay Predictor AI", layout="centered")
st.title("🔥 Parlay Predictor AI")
st.caption("LIVE TNF Props • Raiders @ Broncos • Nov 6, 2025")

st.warning("For entertainment only. 18+. Gamble responsibly.")

if st.button("🚀 Generate Parlay - LIVE TNF"):
    with st.spinner("Pulling DraftKings/FanDuel props..."):
        event = get_upcoming_events_with_props()[0]
        st.success(f"**Thursday Night Football**")
        st.write(f"**{event['away']} @ {event['home']}**")
        st.write("Kickoff: Nov 6, 2025 • 6:15 PM ET • Prime Video")
        
        props = get_player_props()
        if props:
            st.subheader("🔥 TOP 10 PLAYER PROPS (LIVE ODDS)")
            for p in props:
                st.write(f"• **{p['player']}** — {p['prop']} @ **{p['odds']}** ({p['book']})")
        else:
            st.info("Props loading... refresh in 5 min")