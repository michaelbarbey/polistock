import os
from dotenv import load_dotenv

load_dotenv()
# API KEYS
CONGRESS_API_KEY = os.getenv("CONGRESS_API_KEY")
GOOGLE_CIVIC_API_KEY = os.getenv("GOOGLE_CIVIC_API_KEY")
NYT_API_KEY = os.getenv("NYT_API_KEY")

if not CONGRESS_API_KEY:
    raise ValueError("CONGRESS_API_KEY not found in environment variables")

# API URLs
GOOGLE_URL = "https://civicinfo.googleapis.com/civicinfo/v2/divisionsByAddress"

CONGRESS_API_URL = f"https://api.congress.gov/v3/"

# TERM DATES URL
LEG_CURRENT_URL = (
    "https://raw.githubusercontent.com/"
    "unitedstates/congress-legislators/main/"
    "legislators-current.yaml"
    )

CAPITOL_TRADES_URL = f"https://www.capitoltrades.com/politicians/"

# capitol trades image url
#CAPITOL_TRADES_IMG = f"https://www.capitoltrades.com/politicians/{politician_id}"


NYT_API_URL = "https://api.nytimes.com/svc/search/v2/articlesearch.json"

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) "
    "Version/26.1 Safari/605.1.15"
)

# Constants
DEFAULT_TRANSACTION_LIMIT = 25
DEFAULT_NEWS_LIMIT = 2