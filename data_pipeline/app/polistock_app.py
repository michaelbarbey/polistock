from services.google_civic_service import GoogleCivicDistrictValue
from services.congress_service import CongressMemberProfile
from services.capitol_trades_service import CapitolTrades
from services.news_service import NewsArticles
#from models import Official


def get_official_data(street, city, state, zipcode):
    
    try:
        # gets district information from google civic service
        
        print(f"fetching district data")
        google_civic =GoogleCivicDistrictValue()
        district = google_civic._fetch_ocd_id(street, city, state, zipcode)
        
        if not district:
            print("failed to fetch district data")
            return None
        
        # gets congress member profile
        print(f"fetching congress member's profile")
        congress_service = CongressMemberProfile()
        official = congress_service.get_congress_member(district)
        
        if not official:
            print("failed to fetch congress member's profile")
            return None
        
        # gets stocks transactions
        capitol_trades = CapitolTrades()
        capitol_trades.scrape_politician(official)
        
        # gets profile image
        print(f"fetching profile image")
        if not official.photo_url:
            # photo_url = capitol_trades.fetch_headshot_url(official)
            # official.photo_url = photo_url
            capitol_trades.fetch_headshot_url(official)
        
        # gets news articles
        print(f"fetching news articles")
        news_articles = NewsArticles()
        
        # counts articles to fetch to limit api calls
        article_count = 0
        max_articles_per_company = 2
        max_total_articles = 8
        
        # avoids duplicate articles
        searched_companies = set()
        
        for transaction in official.transactions[:5]:
            if article_count >= max_total_articles:
                break
            
            company = transaction.company
            
            # skips if already searched
            if company in searched_companies:
                continue
            searched_companies.add(company)
            print(f"searching articles for: {company}")
            
            # fetch time
            articles = news_articles.get_articles(
                company_name=company,
                traded_date=transaction.traded_date,
                limit=max_articles_per_company
            )
            
            # link articles to official
            for article in articles:
                if article_count >= max_total_articles:
                    break
                official.officials_articles(article)
                article_count += 1
        print(f"total articles found: {article_count}")
    
        # log output
        print(f"profile data")
        print(f"Official: {official.fullname}")
        print(f"Party: {official.party}")
        print(f"District: {district.state_code}-{district.district_code}")
        print(f"Transactions: {len(official.transactions)}")
        print(f"Articles: {len(official.articles)}")
        if official.contact:
            print(f"Contact: {official.contact.phone_number}")
        
        # api response
        return official.to_dict()
    
    except Exception as e:
        print(f"Error in get_official_data: {e}")
        import traceback
        traceback.print_exc()
        return None

def run_polistock():
    print("polidemos running...")
    
    # user input
    street = input("street: ")
    city = input("city: ")
    state = input("state: ")
    zipcode = input("zip code: ")
    
    # fetch data
    result = get_official_data(street, city, state, zipcode)
    
    if result:
        print("success")
        print(f"data fetched:",
              f"official: {result['fullname']}")
        return result
    else:
        print("failed to fetch data")
        return None

def get_official_by_address(address_data):
    return get_official_data(
        street=address_data.get('street', ''),
        city=address_data['city'],
        state=address_data['state'],
        zipcode=address_data['zipcode']
    )

if __name__ == "__main__":
    run_polistock()