
# classes structure for representative data model

# representative: official class
class Official:
    def __init__(self, name, party, chamber, district, state, age, term_start, term_end, photo_url):
        self.name = name
        self.party = party
        self.chamber = chamber
        self.district = district
        self.state = state
        self.age = age
        self.term_start = term_start
        self.term_end = term_end
        self.photo_url = photo_url
        self.transactions = []
        
    def add_transaction(self, transaction):
        self.transactions.append(transaction)
