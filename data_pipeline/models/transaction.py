# member's transactional activity data
class Transaction:
    def __init__ (
        self,
        company,
        ticker_symbol,
        published_date,
        traded_date,
        transaction_type,
        stock_price
    ):
        self.company = company
        self.ticker_symbol = ticker_symbol
        self.published_date = published_date
        self.traded_date = traded_date
        self.transaction_type = transaction_type
        self.stock_price = stock_price
    
    # for debugging
    def __repr__(self):
        return (f"Transaction(company={self.company!r}, "
                f"ticker={self.ticker_symbol!r}, "
                f"type={self.transaction_type!r}, "
                f"date={self.traded_date!r})")
    
    # quick output
    def __str__(self):
        ticker = f"({self.ticker_symbol})" if self.ticker_symbol else ""
        return f"{self.transaction_type} {self.company} {ticker} on {self.traded_date}"
