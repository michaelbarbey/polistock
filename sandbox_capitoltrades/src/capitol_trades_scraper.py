# class CapitolTradesScraper, naviggates through CapitolTrades website to collect data from the data table

from algorithms.sorting import merge_sort
from utils.txn_keys import key_value_bin
from services.profile_data import fetch_official_profile
from services.bioguide_data import fetch_term_dates
from models.representative import Official
from models.transaction import Transaction
from services.transaction_data import get_transaction_data

import re
import time
from difflib import get_close_matches
import requests
from bs4 import BeautifulSoup


class CapitolTradesScraper:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/605.1.15 (KHTML, like Gecko) "
                "Version/26.1 Safari/605.1.15"
            ),
            "Accept-Language": "en-US,en;q=0.9",
        }

    # --------------------------
    # 1) Find politician ID
    # --------------------------
    def _fetch_politician_directory_page(self, page: int) -> str:
        # NOTE: their directory paginates; this works today, but if they change it,
        # you’ll detect it quickly because no /politicians/<ID> links will appear.
        url = "https://www.capitoltrades.com/politicians"
        r = self.session.get(url, params={"page": page}, headers=self.headers, timeout=30)
        r.raise_for_status()
        return r.text

    def _discover_politicians(self, max_pages: int = 25):
        """
        Returns list of dicts: [{"name": "...", "id": "P000608"}, ...]
        We harvest from hrefs like /politicians/M001236 which are present in HTML.  [oai_citation:1‡Capitol Trades](https://www.capitoltrades.com/politicians/M001236)
        """
        people = []
        seen = set()

        for page in range(1, max_pages + 1):
            html = self._fetch_politician_directory_page(page)
            soup = BeautifulSoup(html, "html.parser")

            # Find links that look like /politicians/<ID>
            for a in soup.find_all("a", href=True):
                href = a["href"]
                m = re.match(r"^/politicians/([A-Z]\d{6})$", href)  # e.g., M001236
                if not m:
                    m = re.match(r"^/politicians/([A-Z]\d{6}|[A-Z]\d{6,})$", href)

                if m:
                    pid = m.group(1)
                    name = a.get_text(strip=True)
                    if name and (pid not in seen):
                        people.append({"name": name, "id": pid})
                        seen.add(pid)

            # If a page yields nothing, stop early (directory likely changed)
            if not people and page >= 2:
                break

            time.sleep(0.2)

        return people

    def _resolve_politician_id(self, query: str) -> str | None:
        people = self._discover_politicians(max_pages=25)
        if not people:
            return None

        names = [p["name"] for p in people]
        if query in names:
            chosen = query
        else:
            matches = get_close_matches(query, names, n=3, cutoff=0.5)
            if not matches:
                return None
            chosen = matches[0]

        for p in people:
            if p["name"] == chosen:
                return p["id"]
        return None

    # --------------------------
    # 2) Scrape politician page
    # --------------------------
    def _fetch_politician_page(self, politician_id: str) -> str:
        url = f"https://www.capitoltrades.com/politicians/{politician_id}"
        r = self.session.get(url, headers=self.headers, timeout=30)
        r.raise_for_status()
        return r.text

    def fetch_trades(self, query: str, max_pages: int = 10):
        """
        Fetch trades for a given politician name query.

        Pipeline:
        - resolve politician id from the /politicians directory
        - fetch politician profile HTML (server-rendered)
        - extract each trade "card" block
        - parse each block using services.transaction_data.get_transaction_data

        Returns list[dict] shaped exactly like get_transaction_data().
        """
        pid = self._resolve_politician_id(query)
        if not pid:
            return []

        html = self._fetch_politician_page(pid)
        soup = BeautifulSoup(html, "html.parser")

        # The trade cards include a link text like "Goto trade detail page."
        trade_blocks = []
        for a in soup.find_all("a", string=re.compile(r"Goto trade detail page", re.I)):
            block = a.find_parent()
            if block:
                trade_blocks.append(block)

        results = []
        for block in trade_blocks:
            d = get_transaction_data(str(block))

            # Ensure we keep the resolved politician id
            if not d.get("bioguide_id"):
                d["bioguide_id"] = pid

            # If the parser couldn't find a name inside the card, use the page header
            if not d.get("official"):
                header = soup.find("h1") or soup.find("h2")
                d["official"] = header.get_text(strip=True) if header else query

            results.append(d)

        return results
    
    def fetch_officials(self, query: str, max_pages: int = 10):
        """Return an Official model populated with sorted Transaction models, or None."""
        trades = self.fetch_trades(query, max_pages=max_pages)
        if not trades:
            return None

        # Collect unique names, prefer an exact match, otherwise closest match
        names = []
        for d in trades:
            name = d.get("official")
            if name and name not in names:
                names.append(name)
        names.sort()
        if not names:
            return None

        if query in names:
            chosen = query
        else:
            matches = get_close_matches(query, names, n=3, cutoff=0.5)
            if not matches:
                return None
            chosen = matches[0]

        rows = [d for d in trades if d.get("official") == chosen]
        if not rows:
            return None

        biog = rows[0].get("bioguide_id")

        # Age & district
        if biog:
            age, district = fetch_official_profile(biog)
        else:
            age, district = (None, None)

        # Term dates
        if biog:
            term_start, term_end = fetch_term_dates(biog)
        else:
            term_start, term_end = (None, None)

        party = rows[0].get("party")
        chamber = rows[0].get("chamber")
        state = rows[0].get("state")

        official = Official(
            name=chosen,
            party=party,
            chamber=chamber,
            district=district,
            state=state,
            age=age,
            term_start=term_start,
            term_end=term_end,
            photo_url=None,
        )

        txns = []
        for d in rows:
            txns.append(
                Transaction(
                    company=d.get("company"),
                    stock_symbol=d.get("ticker"),
                    transaction_type=d.get("txn_type"),
                    value_range=d.get("value_range"),
                    date=d.get("date"),
                    price=d.get("price"),
                )
            )

        official.transactions = merge_sort(txns, key_func=key_value_bin, reverse=False)
        return official