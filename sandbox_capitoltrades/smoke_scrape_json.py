import requests
import time

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.1 Safari/605.1.15"

HEADERS = {
    "User-Agent": UA,
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Origin": "https://www.capitoltrades.com",
    "Referer": "https://www.capitoltrades.com/",
}

def main():
    s = requests.Session()

    # 0) Confirm we can reach the main site (HTML)
    r0 = s.get("https://www.capitoltrades.com/trades", headers={"User-Agent": UA}, timeout=30)
    print("Main site status:", r0.status_code, "| content-type:", r0.headers.get("content-type"))

    # 1) Confirm we can get JSON from BFF issuers endpoint
    issuers_url = "https://bff.capitoltrades.com/issuers"
    r1 = s.get(issuers_url, params={"search": "apple"}, headers=HEADERS, timeout=30)
    print("\nIssuers status:", r1.status_code, "| content-type:", r1.headers.get("content-type"))
    if r1.ok:
        data = r1.json()
        print("Issuers JSON type:", type(data))
        # show first few entries, structure-dependent
        if isinstance(data, list):
            print("Issuers sample[0]:", data[0] if data else None)
        else:
            print("Issuers keys:", list(data.keys())[:20])
    else:
        print("Issuers body (first 200):", r1.text[:200])

    # 2) Attempt trades JSON endpoint (may be blocked/503)
    # Some sources suggest /trades supports per_page/pageSize/page.
    trades_url = "https://bff.capitoltrades.com/trades"
    params = {"page": 1, "pageSize": 12, "per_page": 12, "q": "Scott Peters"}

    for attempt in range(1, 4):
        r2 = s.get(trades_url, params=params, headers=HEADERS, timeout=30)
        print(f"\nTrades attempt {attempt} status:", r2.status_code, "| content-type:", r2.headers.get("content-type"))
        if r2.status_code == 200 and "application/json" in (r2.headers.get("content-type") or ""):
            tj = r2.json()
            print("Trades keys:", list(tj.keys())[:30] if isinstance(tj, dict) else type(tj))
            # try to display one item if present
            if isinstance(tj, dict):
                for k in ("data", "items", "results", "trades"):
                    if isinstance(tj.get(k), list) and tj.get(k):
                        print(f"Trades sample item from '{k}':", tj[k][0])
                        break
            return
        if r2.status_code in (429, 503):
            time.sleep(2)
            continue
        print("Trades body (first 200):", r2.text[:200])
        break

if __name__ == "__main__":
    main()
