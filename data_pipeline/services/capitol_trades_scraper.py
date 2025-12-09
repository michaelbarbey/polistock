# class CapitolTradesScraper, naviggates through CapitolTrades website to collect data from the data table

from difflib import get_close_matches
import requests
from bs4 import BeautifulSoup

from utils.algorithms.sorting import merge_sort
from utils.txn_keys import key_value_bin
from services.profile_data import fetch_official_profile
from services.bioguide_data import fetch_term_dates
from models.representative import Official
from models.transaction import Transaction
from services.transaction_data import get_transaction_data

class CapitolTradesScraper:
    def __init__(self, base_url="https://www.capitoltrades.com/trades"):
        self.base_url = base_url
        self.headers ={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/58.0.3029.110 Safari/537.3"
            )
        }

    # fetch raw trades  
    def fetch_trades(self, query, max_pages=10):
        all_results = []

        # page = 1 testing page numbers
        for page in range(1, max_pages + 1):
            url = f"{self.base_url}?q={query}&page={page}"
            # print(f"Fetching data from page {page} -- Status:")  # testing page outputs

            try:
                response = requests.get(url, headers=self.headers)
                response.raise_for_status()  # raise for bad responses
               # print(response.status_code)  # testing page outputs
            except requests.RequestException as e:
                print(f"Error fetching data page: {page}, {e}")  # error handling
                break

            soup = BeautifulSoup(response.text, 'html.parser')
            # looping through the table
            rows = soup.find_all('tr')

            if len(rows) <= 1:
                print("No trade rows found.")
                break

            trade_rows = rows[1:]  # skips the header
            for row in trade_rows:
                txn = get_transaction_data(str(row))
                if txn:
                    all_results.append(txn)

            # ending condition based on number of rows (12 per page)
            if len(trade_rows) < 12:
                print("No more trade rows found. Ending the loop.")
                break

        return all_results
    

    # fetching officials by name
    def fetch_officials(self, query, max_pages=10):
        # fetching raw trades data
        trades = self.fetch_trades(query, max_pages)
        if not trades:
            return None

        # sorting unique names
        names = []
        for d in trades:
            name = d.get('official')
            if name and name not in names:
                names.append(name)
        names.sort()
        if not names:
            return None

        # match names
        if query in names:
            chosen = query
        else:
            matches = get_close_matches(query, names, n=3, cutoff=0.5)
            if matches:
                chosen = matches[0]
            else:
                return None

        # filter rows for the chosen official
        rows = []
        for d in trades:
            if d.get('official') == chosen:
                rows.append(d)

        if not rows:
            return None
        
        # bioguide ID for profile lookups
        biog = rows[0].get('bioguide_id')

        # age & district
        if biog:
            age, district = fetch_official_profile(biog)
        else:
            age, district = (None, None)
            

        # term dates
        if biog:
            term_start, term_end = fetch_term_dates(biog)
            #print(f"DEBUG → bioguide_id: {biog!r}, term_start: {term_start!r}, term_end: {term_end!r}")
        else:
            term_start, term_end = (None, None)
           # print(f"DEBUG → bioguide_id: {biog!r}, term_start: {term_start!r}, term_end: {term_end!r}")

        # party, chamber, state from the first row
        party   = rows[0].get('party')
        chamber = rows[0].get('chamber')
        state   = rows[0].get('state')

        # building Official object
        official = Official(
            name       = chosen,
            party      = party,
            chamber    = chamber,
            district   = district,
            state      = state,
            age        = age,
            term_start = term_start,
            term_end   = term_end,
            photo_url  = None
        )

        # building transactions
        txns = []
        for d in rows:
            txn = Transaction(
                company             = d.get('company'),
                stock_symbol        = d.get('ticker'),
                transaction_type    = d.get('txn_type'),
                value_range         = d.get('value_range'),
                date                = d.get('date'),
                price               = d.get('price')
            )
            txns.append(txn)

        # sort the transactions by value‐bin order
        official.transactions = merge_sort(
            txns,
            key_func = key_value_bin,  # bin price key
            reverse  = False
        )

        return official