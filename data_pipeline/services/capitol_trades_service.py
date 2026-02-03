# CapitolTrades Module Reconfigure to use the Official Object instead and perform a single scrape so it can get the profile headshot as well.

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from models.official import Official
from models.transaction import Transaction
from utils.date_helpers import format_date
from config.settings import CAPITOL_TRADES_URL, USER_AGENT, DEFAULT_TRANSACTION_LIMIT

class CapitolTrades:
    
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            "User-Agent": USER_AGENT,
            "Accept-Language": "en-US,en;q=0.9",
        }
        self.base_url = CAPITOL_TRADES_URL
    
    def scrape_politician(self, official, limit=DEFAULT_TRANSACTION_LIMIT):
        
        try:
            politician_id = official.bioguide_id
            print(f"member identifier: {politician_id}")
        
            url = f"{self.base_url}/{politician_id}?pageSize=96"
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            # grabs the first tbody on the page
            tbody = soup.find("tbody")
            if not tbody:
                print("No transaction table found on page.")
                return official

            rows = tbody.find_all("tr")
            print(f"Found {len(rows)} transaction rows")
            
            transaction_count = 0
            for tr in rows[:limit]:
                try:
                    tds = [td.get_text(" ", strip=True) for td in tr.find_all("td")]
                    if not tds or len(tds) < 6:
                        continue
                
                    # extracting txn data
                    company = tds[0]
                    ticker_symbol = self._extract_ticker(company)
                    published_date = format_date(tds[1])
                    traded_date = format_date(tds[2])
                    transaction_type = tds[4].lower()  # 'buy', 'sell',
                    stock_price = tds[5]
                
                    # transaction object
                    transaction = Transaction(
                        company=company,
                        ticker_symbol=ticker_symbol,
                        published_date=published_date,
                        traded_date=traded_date,
                        transaction_type=transaction_type,
                        stock_price=stock_price
                        )
                
            # article begin date: ('days 21',), ('2 Dec 2025',), Suozzi, Thomas R., ('US TREASURY BILLS N/A',)
            # {'company': ('US TREASURY BILLS N/A',), 'ticker_symbol': ('10 Nov 2025',), 'published_date': ('2 Dec 2025',), 'traded_date': ('days 21',), 'transaction_type': ('buy',), 'stock_price': '15K–50K'}
            
                    official.officials_transaction(transaction)
                    transaction_count += 1
            
                except Exception as e:
                    print(f"error parsing transaction row: {e}")
                    continue
                
            print(f"Successfully scraped {transaction_count} transactions")
            return official
    
        except requests.exceptions.RequestException as e:
            print(f"Error scraping Capitol Trades: {e}")
            return official
    
        except Exception as e:
            print(f"Unexpected error in scrape_politician: {e}")
            import traceback
            traceback.print_exc()
            return official
    
    # get headshot
    def fetch_headshot_url(self, official):
        try:
            politician_id = official.bioguide_id
            page_url = f"{self.base_url}/{politician_id}"
            print(f"profile image: {politician_id}")
            
            response = requests.get(page_url, headers=self.headers, timeout=30)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            # multiple selectors to collect image url
            img = (
                soup.select_one("article.politician-detail-card header figure img") or
                soup.select_one("figure img") or
                soup.select_one("img.politician-photo") or
                soup.find("img", class_=lambda x: x and "politician" in x.lower() if x else False)
            )

            if not img:
                print("member's profile image not found")
                return official.dict()
            
            # image src
            src = img.get("src") or img.get("data-src")
            if not src:
                print("image element found but no src")
                return official.dict()
            
            # handle relative URLs safely
            photo_url = urljoin(page_url, src)
            official.photo_url = photo_url
            print(f"member img: {photo_url}")
            return official
        
        except requests.exceptions.RequestException as e:
            print(f"Error fetching headshot: {e}")
            return official
        except Exception as e:
            print(f"Unexpected error in fetch_headshot: {e}")
            import traceback
            traceback.print_exc()
            return official
        
    def _extract_ticker(self, company_string):
        if not company_string or "N/A" in company_string:
            return None
        
        parts = company_string.split()
        if len(parts) > 1:
            potential_ticker = parts[-1].split(":")[0]  # Handle "TSLA:US" format
            # tickers are between 1 - 5 charcatrs
            if potential_ticker.isupper() and 1 <= len(potential_ticker) <= 5:
                return potential_ticker