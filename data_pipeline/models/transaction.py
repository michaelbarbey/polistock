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