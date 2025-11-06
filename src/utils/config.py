import os
from dotenv import load_dotenv

load_dotenv()

SPORTSDATAIO_KEY = os.getenv("SPORTSDATAIO_KEY")
ODDS_API_KEY = os.getenv("ODDS_API_KEY")

if not SPORTSDATAIO_KEY or not ODDS_API_KEY:
    raise ValueError("Missing API keys in .env or Streamlit secrets!")