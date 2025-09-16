import os
from pathlib import Path
import yfinance as yf
import json
from dotenv import load_dotenv

load_dotenv()

BATCH_SIZE = 30

def fetch_info(ticker: str):
    try:
        return yf.Ticker(ticker).info
    except Exception as e:
        print(f"Error fetching quote for {ticker}: {e}")
        return {}


def get_stocks(
        
):
    stocks = []

    output_file="stocks.json"
    # Ensure JSON file exists
    if not Path(output_file).exists():
        with open(output_file, "w") as f:
            json.dump({}, f)

    with open(output_file, "r") as f:
        all_data = json.load(f)
    
    with open("tickers_nyse.json", "r") as f:
        ticker_info = json.load(f)
        all_tickers = ticker_info['tickers']
        index = ticker_info['last_index']

    batch = all_tickers[index:index + BATCH_SIZE] # Process next batch
    real_batch_size = len(batch)

    if real_batch_size < BATCH_SIZE:
        remaining = BATCH_SIZE - real_batch_size
        batch += all_tickers[:remaining]

    for symbol in batch:
        info = fetch_info(symbol)
        print(f"Fetched info for {symbol}")  # Print first 100 chars


        metrics = {
            "price": info.get("currentPrice"),
            "pe_ratio": info.get("trailingPE"),
            "ps_ratio": info.get("priceToSalesTrailing12Months"),
            "peg_ratio": info.get("trailingPegRatio"),
            "revenue_growth": info.get("revenueGrowth"),
            "earnings_growth": info.get("earningsGrowth"),
            "de_ratio": info.get("debtToEquity"),
            "average_analyst_rating": info.get("averageAnalystRating"),
        }

        # Save ticker as key
        all_data[symbol] = metrics

    # Update index pointer
    ticker_info["last_index"] = remaining if real_batch_size < BATCH_SIZE else index + BATCH_SIZE

    with open(output_file, "w") as f:
        json.dump(all_data, f, indent=2)

    with open("tickers_nyse.json", "w") as f:
        json.dump(ticker_info, f, indent=2)

    print(f"✅ Saved {len(batch)} stocks to {output_file}")

    return stocks
