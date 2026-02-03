# member's profile

from models.transaction import Transaction
from models.district import District
from models.article import Article

class Official: # Transaction may not need to be passed in tbis structure
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
        photo_url=None,  # made optional with default
    ):
        # official personal values
        self.firstname = firstname
        self.lastname = lastname
        self.fullname = fullname
        self.bioguide_id = bioguide_id
        
        # official political information
        self.party = party
        self.chamber = chamber
        self.term_start = term_start
        self.term_end = term_end
        
        # media attributes
        self.photo_url = photo_url
        
        # additonal class values
        self.districts = []
        self.transactions = []
        self.articles = []
        self.contact = None
        
    def officials_district(self, district):
        
        # district (District): District object to add
        if not isinstance(district, District):
            raise TypeError(f"Expected District object, got {type(district)}")
        self.districts.append(district)
    
    def officials_transaction(self,transaction):
        # method to add transaction to official
        # transaction (Transaction): Transaction object to add
        if not isinstance(transaction, Transaction):
            raise TypeError(f"Expected Transaction object, got {type(transaction)}")
        self.transactions.append(transaction)
        
    def officials_articles(self, article):
        # article (Article): Article object to add
        if not isinstance(article, Article):
            raise TypeError(f"Expected Article object, got {type(article)}")
        self.articles.append(article)
        
    def __str__(self):
        """Human-readable string"""
        return f"{self.fullname} ({self.party}) - {self.chamber}"
        
    # to server
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
            "contact": self.contact.to_dict() if self.contact else None,
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
                    "article_image": a.article_image,
                    "article_link": a.article_link,
                    "author": a.author
                }
                for a in self.articles
            ],
        }
        
    # utility methods
    
    # gets total number of transactions
    def get_transaction_count(self):
        return len(self.transactions)
    
    # get total number of articles
    def get_article_count(self):
        
        return len(self.articles)
    
    # quick object details
    def print_summary(self):
        print(f"Official: {self.fullname}")
        print(f"Party: {self.party}")
        print(f"Chamber: {self.chamber}")
        print(f"Bioguide ID: {self.bioguide_id}")
        print(f"Term: {self.term_start} to {self.term_end}")
        print(f"\nDistrict: {(self.districts)}")
        print(f"Transactions: {len(self.transactions)}")
        print(f"Articles: {len(self.articles)}")