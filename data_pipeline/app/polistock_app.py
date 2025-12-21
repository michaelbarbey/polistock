from services.google_civic_service import GoogleCivicDistrictValue
from services.congress_service import CongressMemberProfile
from services.capitol_trades_service import CapitolTrades
from services.news_service import NewsArticles
#from models import Official

def run_polistock():
    # this script can be stored as it's file function
    # get's user input and district number returns an object with location info

    user_address = [
        "street ",
        "city ",
        "state ",
        "zipcode "
    ]

    street = "121 highwood rd"
    city = "east williston"
    state_name = "new york"
    state_code = "ny"
    zipcode = "11596"

    for request in user_address:
        user_input = input(f"{request}")
        if request == "street":
            street = user_input
        elif request == "city":
            city = user_input
        elif request == "state":
            state_code = user_input
        elif request == "zipcode":
            zipcode = user_input
    
    # returns district object
    google_civic = GoogleCivicDistrictValue()
    district_profile = google_civic._fetch_ocd_id(street,city, state_name, zipcode)

    # accesses Official class
    congress_member = CongressMemberProfile()
    congress_profile = congress_member.get_congress_member(district_profile)

    # initiates transactions profile
    capitol_activity = CapitolTrades()
    
    # congress object
    member_profile = congress_profile

    # returns a list of transaction objects
    transaction_data = capitol_activity.scrape_politician(member_profile) # removed limits parameter, if fails call from settings

    # capitol_transactions = {
    #     "company" : "",
    #     "ticker_symbol" : "",
    #     "published_date" : "",
    #     "traded_date" : "",
    #     "transaction_type" : "",
    #     "stock_price": ""
    # }

    # FLAG: may be an issue with import 
    transactions_list = transaction_data.transactions

    # for items in transactions_list:
    #     print(items.company)
    # transactions = []
    # for transaction in transaction_data:
        # print(transactions)
        # company = transaction.company
        # ticker_symbol = transaction.ticker_symbol
        # published_date = transaction.published_date
        # traded_date = transaction.traded_date
        # transaction_type=transaction.transaction_type
        # stock_price = transaction.stock_price
        # congress_profile.officials_transaction(
        #     company=company,
        #     ticker_symbol=ticker_symbol,
        #     published_date=published_date,
        #     traded_date=traded_date,
        #     transaction_type=transaction_type,
        #     stock_price=stock_price
        # )
    # print(congress_profile.fullname)
    # print(congress_profile.transactions[1].stock_price)

    # for items in congress_profile.transactions:
    #     print(vars(items))
        
    profile_img = capitol_activity.fetch_headshot_url(congress_profile)
    member_photo = congress_profile.photo_url
    member_photo = profile_img

    article_from = transactions_list[0].traded_date
    article_to = transactions_list[0].published_date
    company_query = transactions_list[0].company #filter
    member_query = congress_profile.fullname

    #relevant_news = NewsArticles(
        # headline= None,
        # article_start =article_from,
        # article_end =article_to,
        # query = company_query,
        # filter_query = member_query,
        # article_short = None,
        # article_image= None
        # )

    # if relevant)news raises errors may be the lack of parameters, uncomment above
    relevant_news = NewsArticles()
    member_news = relevant_news.execute(
        article_begin_date =article_from,
        article_end_date =article_to,
        query = company_query,
        filter_query = member_query,
    )
    top_stories = relevant_news.to_parse(member_news)

    member_top_stories = congress_profile.officials_articles(
        headline=top_stories[0],
        article_start=article_from,
        article_end=article_to,
        filter_query= company_query,
        query = member_query,
        article_short= None,
        article_image=top_stories[1]
    )

    print(f"District: {congress_profile.districts[0].district_code}")
    print(f"\nTransactions: {len(congress_profile.transactions)}")
    print(f"Articles: {len(congress_profile.articles)}")
    
    to_server = congress_profile.to_dict()
    print(to_server)
    return to_server