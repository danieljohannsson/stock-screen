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

def get_stocks(symbols: list[str]):
    stocks = []

    for symbol in symbols:
        quote = fetch_quote(symbol)
        metrics = fetch_metrics(symbol)

        pe = metrics.get("metric", {}).get("peBasicExclExtraTTM")
        pb = metrics.get("metric", {}).get("pbAnnual")
        revenue_growth = metrics.get("metric", {}).get("revenueGrowthTTMYoy")
        price = quote.get("c")

        stocks.append({
            "symbol": symbol,
            "price": price,
            "pe_ratio": pe,
            "pb_ratio": pb,
            "revenue_growth": revenue_growth
        })

    return stocks

# def get_undervalued_stocks(symbols: list[str]):
#     undervalued = []

#     for symbol in symbols:
#         quote = fetch_quote(symbol)
#         metrics = fetch_metrics(symbol)

#         m = metrics.get("metric", {})
#         pe = m.get("peBasicExclExtraTTM")
#         pb = m.get("pbAnnual")
#         roe = m.get("roeAnnual")
#         debt_equity = m.get("totalDebt/totalEquityAnnual")
#         price = quote.get("c")

#         if not all([pe, pb, roe, debt_equity, price]):
#             continue

#         if pe < 15 and pb < 1 and roe > 10 and debt_equity < 0.5:
#             score = (roe / pe) + (1 - debt_equity)  # Custom value formula

#             undervalued.append({
#                 "symbol": symbol,
#                 "price": price,
#                 "pe_ratio": pe,
#                 "pb_ratio": pb,
#                 "roe": roe,
#                 "de_ratio": debt_equity,
#                 "score": round(score, 2)
#             })

#     # Optionally sort by score
#     undervalued.sort(key=lambda x: x["score"], reverse=True)

#     return undervalued
