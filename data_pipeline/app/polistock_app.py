# class Polistock App

from services.capitol_trades_scraper import CapitolTradesScraper
from utils.data_structures.stack import Stack
from utils.data_structures.bst import TransactionBST
from utils.algorithms.sorting import merge_sort
from utils.txn_keys import key_date, key_value_bin, key_company, key_type, key_price
from utils.table_formatting import calculate_column_widths, format_row_with_widths
from config.sort_options import SORT_OPTIONS

class Polistock:
    def __init__(self, api_key=None):
        # initialize scraper, news fetcher, and image finder
        self.scraper       = CapitolTradesScraper()
    #    self.news_fetcher  = NewsFetcher(api_key)
    #    self.image_finder  = ImageFinder()
        self.history = Stack()

    def run(self):
        while True:
            # prompt user
            name = input("Enter the name of the official: ['exit' to quit | 'back' to previous] ").strip()

            if name.lower() == 'back':
                previous = self.history.pop()
                if previous:
                    print()
                    print("Going back to previous official:")
                    print()
                    print(f"Name: {previous.name}")
                    self.display_results(previous, news=[])
                else:
                    print("History is empty.\n")
                continue

            if name.lower() == 'exit':
                print("Thank you for using Polistock. Goodbye!")
                break

            # fetching data for the official
            print(f"Fetching data for {name}...")
            official = self.scraper.fetch_officials(name)
            if not official:
                print(f"No data found for '{name}'. Try again.")
                continue

            print()  # blank line for readability
            # pushing to official object onto the stack
            self.history.push(official)


            # asking user how to sort
            print("How would you like to sort the transactions?")
            for option in SORT_OPTIONS:
                label = SORT_OPTIONS[option][0]
                print(f"{option}. {label}")
            choice = input("Enter the number of your choice: ").strip()
            if choice not in SORT_OPTIONS:
                print("Invalid choice. Default sorting applied.")
                choice = "1"  # default to sort by date

            if choice == "1":  # date sort
                # builds a BST keyed on date
                tree = TransactionBST(key_date)
                for txn in official.transactions:
                    tree.insert(txn)
                # gets newest‑first by reverse inorder
                official.transactions = tree.inorder(reverse=True)

            else:
                # falls back to generic merge_sort
                lbl, key_fn, rev = SORT_OPTIONS[choice]
                official.transactions = merge_sort(
                    official.transactions,
                    key_func = key_fn,
                    reverse  = rev
                )

            # unpacking chosen sort
            lbl   = SORT_OPTIONS[choice][0]
            key_fn = SORT_OPTIONS[choice][1]
            rev    = SORT_OPTIONS[choice][2]

            # perform the sort
            official.transactions = merge_sort(
                official.transactions,
                key_func = key_fn,
                reverse  = rev
            )
            print()

            print(f"Sorting transactions by {lbl}:")
            print()

            # fetching news articles & headshot
            news      = None #self.news_fetcher.fetch_news(official.name)
            photo_url = None #self.image_finder.fetch_headshot(official.name)
            official.photo_url = None #photo_url

            # displays output
            self.display_results(official, news=None)

    def display_results(self, official, news):
        print(f'Elected Official Information')
#        self.display_image(official)

        print()
        print(f"Name: {official.name}")
        print(f"{official.party} | {official.chamber}")
        print(f"District: {official.district}, {official.state}")
        print(f"Term: {official.term_start} to {official.term_end}")
        print(f"Age: {official.age}")
        print(f"Photo URL: {official.photo_url}")
        print()

        print("Transactions:")  # txn: transaction
        print()

        table_rows = []
        if official.transactions:
            for txn in official.transactions:
                # build each cell as a string
                date_str     = txn.date or ""
                type_str     = txn.transaction_type or ""
                symbol_str   = txn.stock_symbol or ""
                company_str  = txn.company or ""
                value_str    = "~$" + (txn.value or "")
                price_str    = f"${txn.price:,.2f}" if isinstance(txn.price, (int, float)) else str(txn.price)
                
                table_rows.append([
                    date_str,
                    type_str,
                    symbol_str,
                    company_str,
                    value_str,
                    price_str
                ])
            
            # compute column widths once
            col_widths = calculate_column_widths(table_rows)

            # now print header (optional)
            print("•  " + format_row_with_widths(
                ["Date", "Type", "Symbol", "Company", "Value", "Price"],
                col_widths
            ))
            print("   " + "-" * (sum(col_widths) + (len(col_widths)-1)*5))

            # print each transaction
            for row in table_rows:
                line = format_row_with_widths(row, col_widths)
                print("•  " + line)
        else:
            print("No transactions found.")


        print()
        print("Recent News Articles:")
        if news:
            for article in news:
                print(f"• {article['title']} ({article['source']})")
                print(f"  {article['url']}")
        else:
            print("No recent news articles found.")