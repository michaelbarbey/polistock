# transactions: processes company's information and gather transaction data

class Transaction:
    def __init__(self, company, stock_symbol, transaction_type, value_range, date, price):
        self.company = company
        self.stock_symbol = stock_symbol
        self.transaction_type = transaction_type
        self.value_range = value_range
        self.date = date
        self.price = price
 
# company: holds company profile details       
class Company:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol