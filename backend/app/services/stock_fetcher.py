import os
import finnhub
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FINNHUB_API_KEY")

# Setup Finnhub client
finnhub_client = finnhub.Client(api_key=API_KEY)

def fetch_quote(symbol: str):
    try:
        return finnhub_client.quote(symbol)
    except Exception as e:
        print(f"Error fetching quote for {symbol}: {e}")
        return {}

def fetch_metrics(symbol: str):
    try:
        return finnhub_client.company_basic_financials(symbol, metric='all')
    except Exception as e:
        print(f"Error fetching metrics for {symbol}: {e}")
        return {}

def get_undervalued_stocks(symbols: list[str]):
    undervalued = []

    for symbol in symbols:
        quote = fetch_quote(symbol)
        metrics = fetch_metrics(symbol)

        pe = metrics.get("metric", {}).get("peBasicExclExtraTTM")
        pb = metrics.get("metric", {}).get("pbAnnual")
        price = quote.get("c")

        if pe and pb and pe < 100 and pb < 60:
            undervalued.append({
                "symbol": symbol,
                "price": price,
                "pe_ratio": pe,
                "pb_ratio": pb
            })

    return undervalued
