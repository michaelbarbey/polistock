from bs4 import BeautifulSoup
from datetime import datetime

# extract transaction data
def get_transaction_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    
    # senate / house representative name
    name_tag = soup.find("h2", class_="politian-name")
    name = name_tag.get_text(strip=True) if name_tag else "N/A"
    
    link = soup.select_one('h2.politian-name a')
    
    # bioguide id; this helps getting an individuals age and disttrict number
    biog_id = None
    if link and link.has_attr('href'):
        biog_id = link['href'].split("/")[-1] # extract bioguide id from URL
    else:
        None
    
    # member's political party
    party_tag = soup.select_one("span.q-field.party")
    party = party_tag.get_text(strip=True) if party_tag else "N/A"
    
    # member's chamber
    chamber_tag = soup.select_one("span.q-field.chamber")
    chamber = chamber_tag.get_text(strip=True) if chamber_tag else "N/A"
    
    # member's state
    state_tag = soup.select_one("span.q-field.us-state-compact")
    state = state_tag.get_text(strip=True) if state_tag else "N/A"
    
    # company name in trasaction
    company_tag = soup.find("h3", class_="q-fieldset issuer-name")
    company = company_tag.get_text(strip=True) if company_tag else "N/A"
    
    # company's ticker symbol
    ticker_tag = soup.find("span", class_="q-field issuer-ticker")
    ticker = ticker_tag.get_text(strip=True) if ticker_tag else "N/A"
    
    # trasnaction type (buy/sell)
    txn_type_tag = soup.select_one("span.q-field.tx-type")
    txn_type = txn_type_tag.get_text(strip=True) if txn_type_tag else "N/A"
    
    # transaction value range
    value_tag = soup.select_one("span.mt-1.text-size-2")
    value_range = value_tag.get_text(strip=True) if value_tag else "N/A"
    
    # transaction date
    cells = soup.find_all("td")
    if len(cells) >= 4:
        date_cell = cells[3] # zero-based: 0= official, 1=company, 2=published, 3=traded
        day_div=date_cell.find("div", class_="text-size3 font-medium")
        yr_div = date_cell.find("div", class_="text-size-2 text-txt-dimmer")
        
        if day_div and yr_div:
            traded_day = day_div.get_text(strip=True)
            traded_year = yr_div.get_text(strip=True)
            
            try:
                dt = datetime.strptime(f"{traded_day} {traded_year}", "%b %d %Y")
                date_str = dt.strftime("%Y-%m-%d")
            except ValueError:
                # fallback to raw if parsing fails
                date_str = f"{traded_day} {traded_year}"
        else:
            date_str = None
    else:
        date_str = None
    
    # transaction price
    price_tag = soup.find("span", string=lambda s: s and s.strip().startswith("$"))
    if price_tag:
        clean = price_tag.text.replace("$", "").replace(",", "").strip()
        try: # locating the individual stock price & cleaning the value to remove symbols.
            price = float(clean)
        except ValueError:
            price = 0.0
    else:
        price = "N/A"
        
    return {
        "official": name,
        "bioguide_id": biog_id,
        "party": party,
        "chamber": chamber,
        "state": state,
        "company": company,
        "ticker": ticker,
        "txn_type": txn_type,
        "value_range": value_range,
        "date": date_str,
        "price": price
    }