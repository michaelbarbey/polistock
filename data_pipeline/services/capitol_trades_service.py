# CapitolTrades Module Reconfigure to use the Official Object instead and perform a single scrape so it can get the profile headshot as well.

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from models.official import Official
from models.transaction import Transaction
#from utils.date_helpers import format_date
from config.settings import CAPITOL_TRADES_URL, USER_AGENT, DEFAULT_TRANSACTION_LIMIT

class CapitolTrades(Official):
    
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            "User-Agent": USER_AGENT,
            "Accept-Language": "en-US,en;q=0.9",
        }
        self.base_url = CAPITOL_TRADES_URL
    
    def scrape_politician(self, official, limit=DEFAULT_TRANSACTION_LIMIT):
        
        politician_id = official.bioguide_id
        print(politician_id)
        
        url = f"{self.base_url}/{politician_id}?pageSize=96"
        r = requests.get(url, headers=self.headers, timeout=30)
        r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")

        # Grab the first tbody on the page (you can tighten this selector once you inspect)
        tbody = soup.find("tbody")
        if not tbody:
            print("No <tbody> found on page.")
            return []

        rows = tbody.find_all("tr")
        results = []
        for tr in rows[:limit]:
            tds = [td.get_text(" ", strip=True) for td in tr.find_all("td")]
            if not tds:
                continue
            results.append(tds)
        
        # article begin date: ('days 21',), ('2 Dec 2025',), Suozzi, Thomas R., ('US TREASURY BILLS N/A',)
        # {'company': ('US TREASURY BILLS N/A',), 'ticker_symbol': ('10 Nov 2025',), 'published_date': ('2 Dec 2025',), 'traded_date': ('days 21',), 'transaction_type': ('buy',), 'stock_price': '15K–50K'}
        
        member_transactions = []
        member_activity = official
        for data in results:
            company = data[0]
            ticker_symbol = None
            published_date=data[1]
            traded_date=data[2]
            transaction_type=data[4]
            stock_price=data[5]
            member_activity.officials_transaction(
                company = company,
                ticker_symbol = ticker_symbol,
                published_date = published_date,
                traded_date = traded_date,
                transaction_type = transaction_type,
                stock_price = stock_price,
            )
            member_transactions.append(member_activity)
        return member_activity
    
    # get headshot
    def fetch_headshot_url(self, official):
        
        politician_id = official.bioguide_id
        page_url = f"{self.base_url}/{politician_id}"
        r = requests.get(page_url, headers=self.headers, timeout=30)
        r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")

        # Robust selector: politician detail card → header → figure → img
        img = soup.select_one(
            "article.politician-detail-card header figure img"
        )

        if not img:
            return None

        src = img.get("src") or img.get("data-src")
        if not src:
            return None
        # handle relative URLs safely
        official.photo_url = urljoin(page_url, src)
        return official