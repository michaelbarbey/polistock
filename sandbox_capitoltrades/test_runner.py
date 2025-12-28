from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]              # polistock-project/
SANDBOX_SRC = Path(__file__).parent / "src"            # sandbox_capitoltrades/src
DATA_PIPELINE = ROOT / "data_pipeline"                 # data_pipeline/

from capitol_trades_scraper import CapitolTradesScraper
from transaction_data import get_transaction_data


sys.path.insert(0, str(SANDBOX_SRC))
sys.path.insert(0, str(DATA_PIPELINE))

def main():
    # 1) Smoke test the parser with a local fixture (no internet)
    fixture = Path(__file__).parent / "fixtures" / "sample_trade_block.html"
    if fixture.exists():
        html = fixture.read_text(encoding="utf-8")
        parsed = get_transaction_data(html)
        print("Fixture parse:", parsed)
    else:
        print("No fixture found yet (that's okay).")

    # 2) Live test scraper (internet)
    s = CapitolTradesScraper()
    name = input("Name to test (e.g., Scott Peters): ").strip()
    trades = s.fetch_trades(name)
    print("Trades found:", len(trades))
    if trades:
        print("First trade:", trades[0])


if __name__ == "__main__":
    main()
