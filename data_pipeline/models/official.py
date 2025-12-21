# member's profile

from models.transaction import Transaction
from models.district import District
from models.article import Article

class Official(Transaction): # Transaction may not need to be passed in tbis structure
    def __init__(
        self, 
        firstname, 
        lastname,
        fullname,
        bioguide_id,
        party, 
        chamber,  
        term_start, 
        term_end, 
        photo_url,
        ):
        
        self.firstname = firstname
        self.lastname = lastname
        self.fullname = fullname
        self.bioguide_id = bioguide_id
        self.party = party
        self.chamber = chamber
        self.term_start = term_start
        self.term_end = term_end
        self.photo_url = photo_url
        self.districts = []
        self.transactions = []
        self.articles = []
        
    def officials_district(
        self,
        city,
        state_code,
        state_name,
        district_code,
        zipcode
        ):
        
        district = District(city, state_code, state_name, district_code, zipcode) 
        self.districts.append(district)
    
    def officials_transaction(
        self,
        company,
        ticker_symbol,
        published_date,
        traded_date,
        transaction_type,
        stock_price,
        ):
        # method to add transaction to official
        
        transaction = Transaction(company, ticker_symbol, published_date, traded_date, transaction_type, stock_price)
        self.transactions.append(transaction)
        
    def officials_articles(
        self,
        headline,
        article_start,
        article_end,
        filter_query,
        query,
        article_short,
        article_image,
    ):
        article = Article(headline, article_start, article_end, filter_query, query, article_short, article_image)
        self.articles.append(article)
        
    def __str__(self):
        """Human-readable string"""
        return f"{self.fullname} ({self.party}) - {self.chamber}"
        
    def to_dict(self):
        """converts to dictionary with nested objects as dicts too"""
        return {
            "firstname": self.firstname,
            "lastname": self.lastname,
            "fullname": self.fullname,
            "bioguide_id": self.bioguide_id,
            "party": self.party,
            "chamber": self.chamber,
            "term_start": self.term_start,
            "term_end": self.term_end,
            "photo_url": self.photo_url,
            "districts": [
                {
                    "district_code": d.district_code,
                    "city": d.city,
                    "state_name": d.state_name,
                    "state_code": d.state_code,
                    "zipcode": d.zipcode
                }
                for d in self.districts
            ],
            "transactions": [
                {
                    "company": t.company,
                    "ticker_symbol": t.ticker_symbol,
                    "published_date": t.published_date,
                    "traded_date": t.traded_date,
                    "transaction_type": t.transaction_type,
                    "stock_price": t.stock_price
                }
                for t in self.transactions
            ],
            "articles": [
                {
                    "headline": a.headline,
                    "article_start": a.article_start,
                    "article_end": a.article_end,
                    "article_image": a.article_image
                }
                for a in self.articles
            ]
        }