import streamlit as st
from src.api.stats_api import get_upcoming_games
from src.api.odds_api import _fetch_props_for_event  # Import internal

st.set_page_config(page_title="Parlay Predictor AI", layout="centered")
st.title("Parlay Predictor AI")
st.caption("AI-powered value parlay builder • MVP v1.2")

st.warning("For entertainment only. 18+. Gamble responsibly.")

if st.button("Generate Parlay"):
    with st.spinner("Fetching live NFL data..."):
        games = get_upcoming_games()
        if not games:
            st.error("No upcoming games. Check SportsDataIO key.")
        else:
            game = games[0]
            st.success(f"**Next Game**: {game['AwayTeam']} @ {game['HomeTeam']} (Week {game['Week']})")

            # TEMP: Use known event ID for LV @ DEN
            event_id = "20251110-den-lv"  # Adjust date if needed
            props = _fetch_props_for_event(event_id)

            if props:
                st.subheader("Top Player Props (Live Odds)")
                for p in props:
                    st.write(f"• **{p['player']}** — {p['prop']} @ **{p['odds']}** ({p['book']})")
            else:
                st.info("No props yet — check back closer to kickoff.")