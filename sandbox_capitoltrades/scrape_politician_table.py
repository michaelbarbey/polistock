import requests
from bs4 import BeautifulSoup

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.1 Safari/605.1.15"

def scrape_politician(politician_id: str, limit: int = 25):
    url = f"https://www.capitoltrades.com/politicians/{politician_id}"
    r = requests.get(url, headers={"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"}, timeout=30)
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

    return results

if __name__ == "__main__":
    pid = input("Politician ID (e.g., P000608): ").strip()
    data = scrape_politician(pid)
    print("rows:", len(data))
    print("first row:", data[0] if data else None)
