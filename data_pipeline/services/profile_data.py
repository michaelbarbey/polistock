from bs4 import BeautifulSoup
import requests
def fetch_official_profile(biouguide_id):
    url = f"https://www.capitoltrades.com/politicians/{biouguide_id}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    
    soup=BeautifulSoup(resp.text, 'html.parser')
    
    # age and district are in <span class='order-1
    spans = soup.find_all("span", class_="order-1 text-center text-size-4 "
                          "group-[.flavour--full]:order-2 "
                          "group-[.flavour--full]:text-size-3")
    
    age = spans[0].get_text(strip=True) if len(spans) > 0 else None
    district = spans[1].get_text(strip=True) if len(spans) > 1 else None
    
    return age, district