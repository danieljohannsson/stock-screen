import os
from pathlib import Path
import yfinance as yf
import json
from dotenv import load_dotenv
from typing import Dict, Any

load_dotenv()

BATCH_SIZE = 30

def calculate_stock_score(stock_data: Dict[str, Any], strategy: str = "balanced") -> float:
    """
    Calculate a comprehensive score for a stock based on the selected strategy.
    Higher scores indicate better investment potential.
    """
    def safe_float(value):
        """Safely convert value to float, return None if conversion fails"""
        if value is None:
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None
    
    if strategy == "value":
        return _calculate_value_score(stock_data, safe_float)
    elif strategy == "growth":
        return _calculate_growth_score(stock_data, safe_float)
    elif strategy == "momentum":
        return _calculate_momentum_score(stock_data, safe_float)
    elif strategy == "quality":
        return _calculate_quality_score(stock_data, safe_float)
    else:  # balanced
        return _calculate_balanced_score(stock_data, safe_float)

def _calculate_balanced_score(stock_data: Dict[str, Any], safe_float) -> float:
    """Balanced approach considering all factors equally"""
    score = 0.0
    
    # P/E Ratio scoring (0-30 points)
    pe_ratio = safe_float(stock_data.get('pe_ratio'))
    if pe_ratio is not None and pe_ratio > 0:
        if pe_ratio <= 15:
            score += 30
        elif pe_ratio <= 25:
            score += 25
        elif pe_ratio <= 35:
            score += 15
        elif pe_ratio <= 50:
            score += 5
        else:
            score += 0
    
    # P/S Ratio scoring (0-20 points)
    ps_ratio = safe_float(stock_data.get('ps_ratio'))
    if ps_ratio is not None and ps_ratio > 0:
        if ps_ratio <= 2:
            score += 20
        elif ps_ratio <= 5:
            score += 15
        elif ps_ratio <= 10:
            score += 10
        elif ps_ratio <= 20:
            score += 5
        else:
            score += 0
    
    # PEG Ratio scoring (0-15 points)
    peg_ratio = safe_float(stock_data.get('peg_ratio'))
    if peg_ratio is not None and peg_ratio > 0:
        if 0.5 <= peg_ratio <= 1.0:
            score += 15
        elif 0.8 <= peg_ratio <= 1.5:
            score += 12
        elif 0.3 <= peg_ratio <= 2.0:
            score += 8
        elif 0.1 <= peg_ratio <= 3.0:
            score += 4
        else:
            score += 0
    
    # Revenue Growth scoring (0-15 points)
    revenue_growth = safe_float(stock_data.get('revenue_growth'))
    if revenue_growth is not None:
        if revenue_growth >= 0.2:
            score += 15
        elif revenue_growth >= 0.1:
            score += 12
        elif revenue_growth >= 0.05:
            score += 8
        elif revenue_growth >= 0:
            score += 4
        else:
            score += 0
    
    # Earnings Growth scoring (0-15 points)
    earnings_growth = safe_float(stock_data.get('earnings_growth'))
    if earnings_growth is not None:
        if earnings_growth >= 0.2:
            score += 15
        elif earnings_growth >= 0.1:
            score += 12
        elif earnings_growth >= 0.05:
            score += 8
        elif earnings_growth >= 0:
            score += 4
        else:
            score += 0
    
    # D/E Ratio scoring (0-10 points)
    de_ratio = safe_float(stock_data.get('de_ratio'))
    if de_ratio is not None:
        if de_ratio <= 0.5:
            score += 10
        elif de_ratio <= 1.0:
            score += 8
        elif de_ratio <= 2.0:
            score += 5
        elif de_ratio <= 5.0:
            score += 2
        else:
            score += 0
    
    # Analyst Rating scoring (0-10 points)
    analyst_rating = stock_data.get('average_analyst_rating')
    if analyst_rating is not None and analyst_rating:
        if 'Strong Buy' in analyst_rating:
            score += 10
        elif 'Buy' in analyst_rating:
            score += 7
        elif 'Hold' in analyst_rating:
            score += 4
        elif 'Sell' in analyst_rating:
            score += 1
        else:
            score += 0
    
    return round(score, 2)

def _calculate_value_score(stock_data: Dict[str, Any], safe_float) -> float:
    """Value investing strategy - focuses on undervalued stocks"""
    score = 0.0
    
    # P/E Ratio (heavily weighted - 0-40 points)
    pe_ratio = safe_float(stock_data.get('pe_ratio'))
    if pe_ratio is not None and pe_ratio > 0:
        if pe_ratio <= 10:
            score += 40
        elif pe_ratio <= 15:
            score += 35
        elif pe_ratio <= 20:
            score += 25
        elif pe_ratio <= 25:
            score += 15
        elif pe_ratio <= 35:
            score += 5
        else:
            score += 0
    
    # P/S Ratio (heavily weighted - 0-30 points)
    ps_ratio = safe_float(stock_data.get('ps_ratio'))
    if ps_ratio is not None and ps_ratio > 0:
        if ps_ratio <= 1:
            score += 30
        elif ps_ratio <= 2:
            score += 25
        elif ps_ratio <= 3:
            score += 20
        elif ps_ratio <= 5:
            score += 10
        else:
            score += 0
    
    # PEG Ratio (moderately weighted - 0-20 points)
    peg_ratio = safe_float(stock_data.get('peg_ratio'))
    if peg_ratio is not None and peg_ratio > 0:
        if peg_ratio <= 0.5:
            score += 20
        elif peg_ratio <= 1.0:
            score += 15
        elif peg_ratio <= 1.5:
            score += 10
        elif peg_ratio <= 2.0:
            score += 5
        else:
            score += 0
    
    # D/E Ratio (moderately weighted - 0-15 points)
    de_ratio = safe_float(stock_data.get('de_ratio'))
    if de_ratio is not None:
        if de_ratio <= 0.3:
            score += 15
        elif de_ratio <= 0.5:
            score += 12
        elif de_ratio <= 1.0:
            score += 8
        elif de_ratio <= 2.0:
            score += 4
        else:
            score += 0
    
    # Revenue Growth (lightly weighted - 0-10 points)
    revenue_growth = safe_float(stock_data.get('revenue_growth'))
    if revenue_growth is not None and revenue_growth >= 0:
        if revenue_growth >= 0.1:
            score += 10
        elif revenue_growth >= 0.05:
            score += 7
        elif revenue_growth >= 0:
            score += 4
        else:
            score += 0
    
    return round(score, 2)

def _calculate_growth_score(stock_data: Dict[str, Any], safe_float) -> float:
    """Growth investing strategy - focuses on high-growth stocks"""
    score = 0.0
    
    # Revenue Growth (heavily weighted - 0-40 points)
    revenue_growth = safe_float(stock_data.get('revenue_growth'))
    if revenue_growth is not None:
        if revenue_growth >= 0.3:
            score += 40
        elif revenue_growth >= 0.2:
            score += 35
        elif revenue_growth >= 0.15:
            score += 30
        elif revenue_growth >= 0.1:
            score += 25
        elif revenue_growth >= 0.05:
            score += 20
        elif revenue_growth >= 0:
            score += 10
        else:
            score += 0
    
    # PEG Ratio (moderately weighted - 0-25 points)
    peg_ratio = safe_float(stock_data.get('peg_ratio'))
    if peg_ratio is not None and peg_ratio > 0:
        if 0.5 <= peg_ratio <= 1.0:
            score += 25
        elif 0.8 <= peg_ratio <= 1.5:
            score += 20
        elif 0.3 <= peg_ratio <= 2.0:
            score += 15
        elif 0.1 <= peg_ratio <= 3.0:
            score += 8
        else:
            score += 0
    
    # D/E Ratio (moderately weighted - 0-20 points)
    de_ratio = safe_float(stock_data.get('de_ratio'))
    if de_ratio is not None:
        if de_ratio <= 0.3:
            score += 20
        elif de_ratio <= 0.5:
            score += 18
        elif de_ratio <= 1.0:
            score += 15
        elif de_ratio <= 2.0:
            score += 10
        elif de_ratio <= 5.0:
            score += 5
        else:
            score += 0
    
    # Analyst Rating (moderately weighted - 0-15 points)
    analyst_rating = stock_data.get('average_analyst_rating')
    if analyst_rating is not None and analyst_rating:
        if 'Strong Buy' in analyst_rating:
            score += 15
        elif 'Buy' in analyst_rating:
            score += 12
        elif 'Hold' in analyst_rating:
            score += 8
        elif 'Sell' in analyst_rating:
            score += 2
        else:
            score += 0
    
    return round(score, 2)

def _calculate_momentum_score(stock_data: Dict[str, Any], safe_float) -> float:
    """Momentum investing strategy - focuses on stocks with strong recent performance"""
    score = 0.0
    
    # Revenue Growth (heavily weighted - 0-35 points)
    revenue_growth = safe_float(stock_data.get('revenue_growth'))
    if revenue_growth is not None:
        if revenue_growth >= 0.25:
            score += 35
        elif revenue_growth >= 0.15:
            score += 30
        elif revenue_growth >= 0.1:
            score += 25
        elif revenue_growth >= 0.05:
            score += 15
        elif revenue_growth >= 0:
            score += 5
        else:
            score += 0
    
    # Earnings Growth (heavily weighted - 0-35 points)
    earnings_growth = safe_float(stock_data.get('earnings_growth'))
    if earnings_growth is not None:
        if earnings_growth >= 0.25:
            score += 35
        elif earnings_growth >= 0.15:
            score += 30
        elif earnings_growth >= 0.1:
            score += 25
        elif earnings_growth >= 0.05:
            score += 15
        elif earnings_growth >= 0:
            score += 5
        else:
            score += 0
    
    # Analyst Rating (moderately weighted - 0-20 points)
    analyst_rating = stock_data.get('average_analyst_rating')
    if analyst_rating is not None and analyst_rating:
        if 'Strong Buy' in analyst_rating:
            score += 20
        elif 'Buy' in analyst_rating:
            score += 15
        elif 'Hold' in analyst_rating:
            score += 8
        elif 'Sell' in analyst_rating:
            score += 2
        else:
            score += 0
    
    # P/E Ratio (lightly weighted - 0-10 points)
    pe_ratio = safe_float(stock_data.get('pe_ratio'))
    if pe_ratio is not None and pe_ratio > 0:
        if pe_ratio <= 30:
            score += 10
        elif pe_ratio <= 40:
            score += 7
        elif pe_ratio <= 60:
            score += 4
        else:
            score += 0
    
    return round(score, 2)

def _calculate_quality_score(stock_data: Dict[str, Any], safe_float) -> float:
    """Quality investing strategy - focuses on financially strong, stable companies"""
    score = 0.0
    
    # D/E Ratio (heavily weighted - 0-35 points)
    de_ratio = safe_float(stock_data.get('de_ratio'))
    if de_ratio is not None:
        if de_ratio <= 0.2:
            score += 35
        elif de_ratio <= 0.4:
            score += 30
        elif de_ratio <= 0.6:
            score += 25
        elif de_ratio <= 1.0:
            score += 15
        elif de_ratio <= 2.0:
            score += 8
        else:
            score += 0
    
    # P/E Ratio (moderately weighted - 0-25 points)
    pe_ratio = safe_float(stock_data.get('pe_ratio'))
    if pe_ratio is not None and pe_ratio > 0:
        if 10 <= pe_ratio <= 20:
            score += 25
        elif 8 <= pe_ratio <= 25:
            score += 20
        elif 5 <= pe_ratio <= 30:
            score += 15
        elif 3 <= pe_ratio <= 40:
            score += 8
        else:
            score += 0
    
    # P/S Ratio (moderately weighted - 0-20 points)
    ps_ratio = safe_float(stock_data.get('ps_ratio'))
    if ps_ratio is not None and ps_ratio > 0:
        if ps_ratio <= 2:
            score += 20
        elif ps_ratio <= 4:
            score += 15
        elif ps_ratio <= 8:
            score += 10
        elif ps_ratio <= 15:
            score += 5
        else:
            score += 0
    
    # Revenue Growth (moderately weighted - 0-15 points)
    revenue_growth = safe_float(stock_data.get('revenue_growth'))
    if revenue_growth is not None and revenue_growth >= 0:
        if revenue_growth >= 0.1:
            score += 15
        elif revenue_growth >= 0.05:
            score += 12
        elif revenue_growth >= 0.02:
            score += 8
        elif revenue_growth >= 0:
            score += 4
        else:
            score += 0
    
    # Analyst Rating (lightly weighted - 0-10 points)
    analyst_rating = stock_data.get('average_analyst_rating')
    if analyst_rating is not None and analyst_rating:
        if 'Strong Buy' in analyst_rating:
            score += 10
        elif 'Buy' in analyst_rating:
            score += 7
        elif 'Hold' in analyst_rating:
            score += 4
        elif 'Sell' in analyst_rating:
            score += 1
        else:
            score += 0
    
    return round(score, 2)

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
            "average_analyst_rating": info.get("averageAnalystRating").split(" - ")[1] if info.get("averageAnalystRating") else None,
            "summary": info.get("longBusinessSummary"),
        }

        # Calculate and add score using balanced strategy
        metrics["balanced_score"] = calculate_stock_score(metrics, "balanced")
        metrics["value_score"] = calculate_stock_score(metrics, "value")
        metrics["growth_score"] = calculate_stock_score(metrics, "growth")
        metrics["momentum_score"] = calculate_stock_score(metrics, "momentum")
        metrics["quality_score"] = calculate_stock_score(metrics, "quality")

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
