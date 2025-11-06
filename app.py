# app.py
import streamlit as st
from src.api.odds_api import get_upcoming_events_with_props, get_player_props

st.set_page_config(page_title="Parlay Predictor AI", layout="centered")
st.title("🔥 Parlay Predictor AI")
st.caption("LIVE TNF Props • Raiders @ Broncos • Nov 6, 2025")

st.warning("For entertainment only. 18+. Gamble responsibly.")

if st.button("🚀 Generate Parlay - LIVE TNF"):
    with st.spinner("Fetching Raiders @ Broncos props..."):
        events = get_upcoming_events_with_props()
        if not events:
            st.error("Game not found — check API date (Nov 5, 2025).")
        else:
            event = events[0]
            st.success(f"**Thursday Night Football**")
            st.write(f"**{event['away']} @ {event['home']}**")
            st.write("Kickoff: Nov 6, 2025 • 6:15 PM ET • Prime Video")
            st.write("Early Line: DEN -9 | O/U 42.5")
            
            props = get_player_props(event["id"])
            if props:
                st.subheader("🔥 TOP 10 PLAYER PROPS (LIVE ODDS)")
                for p in props:
                    st.write(f"• **{p['player']}** — {p['prop']} @ **{p['odds']}** ({p['book']})")
            else:
                st.info("Props not posted yet — refresh in 1 hour (books update ~24h pre-kickoff).")