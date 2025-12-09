# key extraction function
# date

from datetime import datetime

def key_date(txn):
    # parsing ISO dates like "2025-05-04"
    return datetime.strptime(txn.date, "%Y-%m-%d")

def key_company(txn):
    # alphabetical by company name
    return txn.company.lower()

type_order = {"buy": 0, "sell": 1}
def key_type(txn):
    # buys before sells
    return type_order.get(txn.transaction_type.lower(), 2)

# defining the bin ordering
value_order = {
    "1K-15K":    1,
    "15K-50K":   2,
    "50K-100K":  3,
    "100K-250K": 4,
    "250K-500K": 5,
    "500K-1M":   6,
    "1M-5M":     7,
    "5M-25M":    8,
    "25M-50M":   9,
    "50M+":     10
}

def key_value_bin(txn):
    # getting numeric rank of the value‐bin (default 0 if missing)
    bin_rank = value_order.get(txn.value, 0)

    # converting price into a float
    p = txn.price
    if isinstance(p, (int, float)):
        price_val = p
    else:
        try:
            price_val = float(p)
        except Exception:
            price_val = 0.0

    # returning a tuple so merge_sort ties on price descending
    return (bin_rank, -price_val)

def key_price(txn):
    # sorting by price only, highest first
    p = txn.price
    if isinstance(p, (int, float)):
        return p
    try:
        return float(p)
    except Exception:
        return 0.0