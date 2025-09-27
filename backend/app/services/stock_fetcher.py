import os
from pathlib import Path
import yfinance as yf
import json
from datetime import datetime
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
    """Balanced approach with binary pass/fail criteria"""
    score = 0.0
    
    # Revenue Growth (20 points) - Must be >5%
    revenue_growth = safe_float(stock_data.get('revenue_growth'))
    if revenue_growth is not None and revenue_growth > 0.05:
        score += 20
    
    # Return on Equity (20 points) - Must be >15%
    roe = safe_float(stock_data.get('roe'))
    if roe is not None and roe > 0.15:
        score += 20
    
    # Debt to Equity (20 points) - Must be between 0 and 1
    de_ratio = safe_float(stock_data.get('de_ratio'))
    if de_ratio is not None and 0 < de_ratio < 1:
        score += 20
    
    # Free Cash Flow (20 points) - Must be >0
    free_cash_flow = safe_float(stock_data.get('free_cash_flow'))
    if free_cash_flow is not None and free_cash_flow > 0:
        score += 20
    
    # PEG Ratio (20 points) - Must be between 0 and 2
    peg_ratio = safe_float(stock_data.get('peg_ratio'))
    if peg_ratio is not None and 0 < peg_ratio < 2:
        score += 20
    
    return round(score, 2)

def _calculate_value_score(stock_data: Dict[str, Any], safe_float) -> float:
    """Value investing strategy with binary pass/fail criteria"""
    score = 0.0
    
    # Revenue Growth (16.7 points) - Must be >5%
    revenue_growth = safe_float(stock_data.get('revenue_growth'))
    if revenue_growth is not None and revenue_growth > 0.05:
        score += 16.7
    
    # Earnings Growth (16.7 points) - Must be >5%
    earnings_growth = safe_float(stock_data.get('earnings_growth'))
    if earnings_growth is not None and earnings_growth > 0.05:
        score += 16.7
    
    # Return on Equity (16.7 points) - Must be >15%
    roe = safe_float(stock_data.get('roe'))
    if roe is not None and roe > 0.15:
        score += 16.7
    
    # Debt to Equity (16.7 points) - Must be between 0 and 1
    de_ratio = safe_float(stock_data.get('de_ratio'))
    if de_ratio is not None and 0 < de_ratio < 1:
        score += 16.7
    
    # Free Cash Flow (16.7 points) - Must be >0
    free_cash_flow = safe_float(stock_data.get('free_cash_flow'))
    if free_cash_flow is not None and free_cash_flow > 0:
        score += 16.7
    
    # PEG Ratio (16.7 points) - Must be between 0 and 1
    peg_ratio = safe_float(stock_data.get('peg_ratio'))
    if peg_ratio is not None and 0 < peg_ratio < 1:
        score += 16.7
    
    return round(score, 2)

def _calculate_growth_score(stock_data: Dict[str, Any], safe_float) -> float:
    """Growth investing strategy with binary pass/fail criteria"""
    score = 0.0
    
    # Revenue Growth (33.3 points) - Must be ≥20%
    revenue_growth = safe_float(stock_data.get('revenue_growth'))
    if revenue_growth is not None and revenue_growth >= 0.20:
        score += 33.3
    
    # D/E Ratio (33.3 points) - Must be between 0 and 5
    de_ratio = safe_float(stock_data.get('de_ratio'))
    if de_ratio is not None and 0 <= de_ratio <= 5:
        score += 33.3
    
    # PEG Ratio (33.3 points) - Must be between 0 and 2
    peg_ratio = safe_float(stock_data.get('peg_ratio'))
    if peg_ratio is not None and 0 < peg_ratio <= 2:
        score += 33.3
    
    return round(score, 2)

def _calculate_momentum_score(stock_data: Dict[str, Any], safe_float) -> float:
    """Momentum investing strategy with binary pass/fail criteria"""
    score = 0.0
    
    # Earnings Growth (33.3 points) - Must be >15%
    earnings_growth = safe_float(stock_data.get('earnings_growth'))
    if earnings_growth is not None and earnings_growth > 0.15:
        score += 33.3
    
    # Revenue Growth (33.3 points) - Must be >10%
    revenue_growth = safe_float(stock_data.get('revenue_growth'))
    if revenue_growth is not None and revenue_growth > 0.10:
        score += 33.3
    
    # Return on Equity (33.3 points) - Must be >20%
    roe = safe_float(stock_data.get('roe'))
    if roe is not None and roe > 0.20:
        score += 33.3
    
    return round(score, 2)

def _calculate_quality_score(stock_data: Dict[str, Any], safe_float) -> float:
    """Quality investing strategy with binary pass/fail criteria"""
    score = 0.0
    
    # PB Ratio (16.7 points) - Must be between 0 and 5
    pb_ratio = safe_float(stock_data.get('pb_ratio'))
    if pb_ratio is not None and 0 < pb_ratio < 5:
        score += 16.7
    
    # Return on Equity (16.7 points) - Must be >15%
    roe = safe_float(stock_data.get('roe'))
    if roe is not None and roe > 0.15:
        score += 16.7
    
    # Debt to Equity (16.7 points) - Must be between 0 and 0.5
    de_ratio = safe_float(stock_data.get('de_ratio'))
    if de_ratio is not None and 0 < de_ratio < 0.5:
        score += 16.7
    
    # Free Cash Flow (16.7 points) - Must be >0
    free_cash_flow = safe_float(stock_data.get('free_cash_flow'))
    if free_cash_flow is not None and free_cash_flow > 0:
        score += 16.7
    
    # Dividend Yield (16.7 points) - Must be >0
    dividend_yield = safe_float(stock_data.get('dividend_yield'))
    if dividend_yield is not None and dividend_yield > 0:
        score += 16.7
    
    # Revenue Growth (16.7 points) - Must be >0
    revenue_growth = safe_float(stock_data.get('revenue_growth'))
    if revenue_growth is not None and revenue_growth > 0:
        score += 16.7
    
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

    ticker_file = "tickers_nyse.json"

    output_file="stocks.json"
    # Ensure JSON file exists
    if not Path(output_file).exists():
        with open(output_file, "w") as f:
            json.dump({}, f)
        with open(ticker_file, "r") as f:
            ticker_info = json.load(f)
            ticker_info['last_index'] = 0
            with open(ticker_file, "w") as f:
                json.dump(ticker_info, f)

    with open(output_file, "r") as f:
        all_data = json.load(f)
    
    with open(ticker_file, "r") as f:
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
            "name": info.get("shortName") if info.get("shortName") else info.get("displayName") ,
            "price": info.get("currentPrice"),
            "pe_ratio": info.get("trailingPE"),
            "ps_ratio": info.get("priceToSalesTrailing12Months"),
            "pb_ratio": info.get("priceToBook"),
            "peg_ratio": info.get("trailingPegRatio"),
            "roe": info.get("returnOnEquity"),
            "dividend_yield": info.get("dividendYield"),
            "free_cash_flow": info.get("freeCashflow"),
            "revenue_growth": info.get("revenueGrowth"),
            "earnings_growth": info.get("earningsGrowth"),
            "de_ratio": info.get("debtToEquity") / 100 if info.get("debtToEquity") else None,
            "average_analyst_rating": info.get("averageAnalystRating").split(" - ")[1] if info.get("averageAnalystRating") else None,
            "summary": info.get("longBusinessSummary"),
            "industry": info.get("industry"),
            "website": info.get("website"),
            "last_fetched": datetime.utcnow().isoformat(),
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

    with open(ticker_file, "w") as f:
        json.dump(ticker_info, f, indent=2)

    print(f"✅ Saved {len(batch)} stocks to {output_file}")

    return stocks
