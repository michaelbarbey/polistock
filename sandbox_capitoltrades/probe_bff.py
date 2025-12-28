import requests

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.1 Safari/605.1.15"
HEADERS = {
    "User-Agent": UA,
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Origin": "https://www.capitoltrades.com",
    "Referer": "https://www.capitoltrades.com/",
}

CANDIDATES = [
    ("issuers", "/issuers", {"search": "apple"}),

    # politician lookup candidates (one of these often exists)
    ("politicians_search", "/politicians", {"search": "Scott Peters"}),
    ("politicians_q", "/politicians", {"q": "Scott Peters"}),
    ("politicians_autocomplete", "/politicians/autocomplete", {"search": "Scott Peters"}),

    # trades candidates (often not exactly /trades)
    ("trades", "/trades", {"q": "Scott Peters", "page": 1}),
    ("transactions", "/transactions", {"q": "Scott Peters", "page": 1}),
    ("disclosures", "/disclosures", {"q": "Scott Peters", "page": 1}),
]

def main():
    s = requests.Session()
    base = "https://bff.capitoltrades.com"

    for name, path, params in CANDIDATES:
        url = base + path
        try:
            r = s.get(url, params=params, headers=HEADERS, timeout=30)
            ctype = r.headers.get("content-type", "")
            print(f"\n{name}: {r.status_code} {ctype}  url={r.url}")
            print("body head:", r.text[:150].replace("\n", " "))

            if r.status_code == 200 and "application/json" in ctype:
                j = r.json()
                if isinstance(j, dict):
                    print("json keys:", list(j.keys())[:20])
                    # show sample row if it has a 'data' list
                    if isinstance(j.get("data"), list) and j["data"]:
                        print("data[0] keys:", list(j["data"][0].keys())[:30])
                elif isinstance(j, list) and j:
                    print("list[0] keys:", list(j[0].keys())[:30] if isinstance(j[0], dict) else type(j[0]))
        except Exception as e:
            print(f"\n{name}: ERROR {e}")

if __name__ == "__main__":
    main()
