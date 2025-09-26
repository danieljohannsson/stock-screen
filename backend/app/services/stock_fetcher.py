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
    """Balanced approach considering all factors with equal weight for comprehensive evaluation"""
    score = 0.0
    
    # Revenue Growth (0-14 points) - Growth potential
    revenue_growth = safe_float(stock_data.get('revenue_growth'))
    if revenue_growth is not None:
        if revenue_growth >= 0.15:
            score += 14
        elif revenue_growth >= 0.10:
            score += 12
        elif revenue_growth >= 0.05:
            score += 10
        elif revenue_growth >= 0.02:
            score += 6
        elif revenue_growth >= 0:
            score += 3
        else:
            score += 0
    
    # Earnings Growth (0-14 points) - Profitability growth
    earnings_growth = safe_float(stock_data.get('earnings_growth'))
    if earnings_growth is not None:
        if earnings_growth >= 0.15:
            score += 14
        elif earnings_growth >= 0.10:
            score += 12
        elif earnings_growth >= 0.05:
            score += 10
        elif earnings_growth >= 0.02:
            score += 6
        elif earnings_growth >= 0:
            score += 3
        else:
            score += 0
    
    # ROE (0-14 points) - Profitability efficiency
    roe = safe_float(stock_data.get('roe'))
    if roe is not None:
        if roe >= 0.20:
            score += 14
        elif roe >= 0.15:
            score += 12
        elif roe >= 0.10:
            score += 10
        elif roe >= 0.05:
            score += 6
        elif roe >= 0:
            score += 3
        else:
            score += 0
    
    # D/E Ratio (0-14 points) - Financial stability
    de_ratio = safe_float(stock_data.get('de_ratio'))
    if de_ratio is not None:
        if de_ratio <= 0.3:
            score += 14
        elif de_ratio <= 0.5:
            score += 12
        elif de_ratio <= 0.8:
            score += 10
        elif de_ratio <= 1.2:
            score += 6
        elif de_ratio <= 2.0:
            score += 3
        else:
            score += 0
    
    # Free Cash Flow (0-14 points) - Financial health
    free_cash_flow = safe_float(stock_data.get('free_cash_flow'))
    if free_cash_flow is not None and free_cash_flow > 0:
        if free_cash_flow >= 2000000000:  # 2B+
            score += 14
        elif free_cash_flow >= 1000000000:  # 1B+
            score += 12
        elif free_cash_flow >= 500000000:  # 500M+
            score += 10
        elif free_cash_flow >= 100000000:  # 100M+
            score += 6
        elif free_cash_flow >= 50000000:   # 50M+
            score += 3
        else:
            score += 0
    
    # PEG Ratio (0-14 points) - Growth-adjusted valuation
    peg_ratio = safe_float(stock_data.get('peg_ratio'))
    if peg_ratio is not None and peg_ratio > 0:
        if 0.5 <= peg_ratio <= 0.8:
            score += 14
        elif 0.3 <= peg_ratio <= 1.0:
            score += 12
        elif 0.8 <= peg_ratio <= 1.2:
            score += 10
        elif 0.1 <= peg_ratio <= 1.5:
            score += 6
        elif 1.2 <= peg_ratio <= 2.0:
            score += 3
        else:
            score += 0
    
    # Analyst Rating (0-16 points) - Market confidence
    analyst_rating = stock_data.get('average_analyst_rating')
    if analyst_rating is not None and analyst_rating:
        if 'Strong Buy' in analyst_rating:
            score += 16
        elif 'Buy' in analyst_rating:
            score += 12
        elif 'Hold' in analyst_rating:
            score += 8
        elif 'Sell' in analyst_rating:
            score += 2
        else:
            score += 0
    
    return round(score, 2)

def _calculate_value_score(stock_data: Dict[str, Any], safe_float) -> float:
    """Value investing strategy - focuses on risk-averse, stable value stocks"""
    score = 0.0
    
    # D/E Ratio (heavily weighted for risk - 0-28 points)
    de_ratio = safe_float(stock_data.get('de_ratio'))
    if de_ratio is not None:
        if de_ratio <= 0.2:
            score += 28
        elif de_ratio <= 0.3:
            score += 24
        elif de_ratio <= 0.5:
            score += 20
        elif de_ratio <= 0.8:
            score += 12
        elif de_ratio <= 1.0:
            score += 6
        else:
            score += 0
    
    # ROE (heavily weighted for profitability - 0-24 points)
    roe = safe_float(stock_data.get('roe'))
    if roe is not None:
        if roe >= 0.20:
            score += 24
        elif roe >= 0.15:
            score += 20
        elif roe >= 0.10:
            score += 16
        elif roe >= 0.05:
            score += 10
        elif roe >= 0:
            score += 4
        else:
            score += 0
    
    # Free Cash Flow (moderately weighted for financial health - 0-16 points)
    free_cash_flow = safe_float(stock_data.get('free_cash_flow'))
    if free_cash_flow is not None and free_cash_flow > 0:
        if free_cash_flow >= 1000000000:  # 1B+
            score += 16
        elif free_cash_flow >= 500000000:  # 500M+
            score += 12
        elif free_cash_flow >= 100000000:  # 100M+
            score += 8
        elif free_cash_flow >= 50000000:   # 50M+
            score += 4
        else:
            score += 0
    
    # PEG Ratio (moderately weighted for growth-adjusted value - 0-12 points)
    peg_ratio = safe_float(stock_data.get('peg_ratio'))
    if peg_ratio is not None and peg_ratio > 0:
        if peg_ratio <= 0.5:
            score += 12
        elif peg_ratio <= 0.8:
            score += 10
        elif peg_ratio <= 1.0:
            score += 6
        elif peg_ratio <= 1.2:
            score += 3
        else:
            score += 0
    
    # Revenue Growth (lightly weighted for stability - 0-8 points)
    revenue_growth = safe_float(stock_data.get('revenue_growth'))
    if revenue_growth is not None:
        if 0.05 <= revenue_growth <= 0.15:  # Moderate, stable growth
            score += 8
        elif 0.02 <= revenue_growth <= 0.20:  # Reasonable growth range
            score += 6
        elif revenue_growth >= 0:  # Any positive growth
            score += 3
        else:
            score += 0
    
    # Earnings Growth (lightly weighted for consistency - 0-6 points)
    earnings_growth = safe_float(stock_data.get('earnings_growth'))
    if earnings_growth is not None:
        if 0.05 <= earnings_growth <= 0.15:  # Moderate, stable earnings growth
            score += 6
        elif 0.02 <= earnings_growth <= 0.20:  # Reasonable earnings growth
            score += 4
        elif earnings_growth >= 0:  # Any positive earnings growth
            score += 2
        else:
            score += 0
    
    # Analyst Rating (lightly weighted for market confidence - 0-6 points)
    analyst_rating = stock_data.get('average_analyst_rating')
    if analyst_rating:
        if 'Strong Buy' in analyst_rating:
            score += 6
        elif 'Buy' in analyst_rating:
            score += 4
        elif 'Hold' in analyst_rating:
            score += 2
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
    """Momentum investing strategy - focuses on stocks with strong recent performance and growth momentum"""
    score = 0.0
    
    # Earnings Growth (heavily weighted - 0-36 points) - Primary momentum indicator
    earnings_growth = safe_float(stock_data.get('earnings_growth'))
    if earnings_growth is not None:
        if earnings_growth >= 0.30:
            score += 36
        elif earnings_growth >= 0.20:
            score += 32
        elif earnings_growth >= 0.15:
            score += 28
        elif earnings_growth >= 0.10:
            score += 22
        elif earnings_growth >= 0.05:
            score += 14
        elif earnings_growth >= 0:
            score += 4
        else:
            score += 0
    
    # Revenue Growth (heavily weighted - 0-32 points) - Secondary momentum indicator
    revenue_growth = safe_float(stock_data.get('revenue_growth'))
    if revenue_growth is not None:
        if revenue_growth >= 0.25:
            score += 32
        elif revenue_growth >= 0.15:
            score += 28
        elif revenue_growth >= 0.10:
            score += 22
        elif revenue_growth >= 0.05:
            score += 14
        elif revenue_growth >= 0:
            score += 4
        else:
            score += 0
    
    # ROE (moderately weighted - 0-18 points) - Profitability momentum
    roe = safe_float(stock_data.get('roe'))
    if roe is not None:
        if roe >= 0.25:
            score += 18
        elif roe >= 0.20:
            score += 15
        elif roe >= 0.15:
            score += 12
        elif roe >= 0.10:
            score += 9
        elif roe >= 0.05:
            score += 5
        elif roe >= 0:
            score += 2
        else:
            score += 0
    
    # Analyst Rating (moderately weighted - 0-14 points) - Market momentum sentiment
    analyst_rating = stock_data.get('average_analyst_rating')
    if analyst_rating is not None and analyst_rating:
        if 'Strong Buy' in analyst_rating:
            score += 14
        elif 'Buy' in analyst_rating:
            score += 11
        elif 'Hold' in analyst_rating:
            score += 5
        elif 'Sell' in analyst_rating:
            score += 1
        else:
            score += 0
    
    return round(score, 2)

def _calculate_quality_score(stock_data: Dict[str, Any], safe_float) -> float:
    """Quality investing strategy - focuses on financially strong, stable companies with quality metrics"""
    score = 0.0
    
    # P/B Ratio (0-14 points) - Book value quality
    pb_ratio = safe_float(stock_data.get('pb_ratio'))
    if pb_ratio is not None and pb_ratio > 0:
        if 0.5 <= pb_ratio <= 1.5:
            score += 14
        elif 0.3 <= pb_ratio <= 2.0:
            score += 12
        elif 0.1 <= pb_ratio <= 3.0:
            score += 9
        elif 0.05 <= pb_ratio <= 4.0:
            score += 6
        elif 1.5 <= pb_ratio <= 5.0:
            score += 3
        else:
            score += 0
    
    # ROE (0-14 points) - Profitability quality
    roe = safe_float(stock_data.get('roe'))
    if roe is not None:
        if roe >= 0.20:
            score += 14
        elif roe >= 0.15:
            score += 12
        elif roe >= 0.10:
            score += 9
        elif roe >= 0.05:
            score += 6
        elif roe >= 0:
            score += 3
        else:
            score += 0
    
    # D/E Ratio (0-14 points) - Financial stability quality
    de_ratio = safe_float(stock_data.get('de_ratio'))
    if de_ratio is not None:
        if de_ratio <= 0.2:
            score += 14
        elif de_ratio <= 0.4:
            score += 12
        elif de_ratio <= 0.6:
            score += 9
        elif de_ratio <= 1.0:
            score += 6
        elif de_ratio <= 2.0:
            score += 3
        else:
            score += 0
    
    # Free Cash Flow (0-14 points) - Financial health quality
    free_cash_flow = safe_float(stock_data.get('free_cash_flow'))
    if free_cash_flow is not None and free_cash_flow > 0:
        if free_cash_flow >= 2000000000:  # 2B+
            score += 14
        elif free_cash_flow >= 1000000000:  # 1B+
            score += 12
        elif free_cash_flow >= 500000000:  # 500M+
            score += 9
        elif free_cash_flow >= 100000000:  # 100M+
            score += 6
        elif free_cash_flow >= 50000000:   # 50M+
            score += 3
        else:
            score += 0
    
    # Dividend Yield (0-14 points) - Income quality
    dividend_yield = safe_float(stock_data.get('dividend_yield'))
    if dividend_yield is not None and dividend_yield > 0:
        if 0.03 <= dividend_yield <= 0.06:  # 3-6% sweet spot
            score += 14
        elif 0.02 <= dividend_yield <= 0.08:  # 2-8% good range
            score += 12
        elif 0.01 <= dividend_yield <= 0.10:  # 1-10% acceptable
            score += 9
        elif dividend_yield >= 0.005:  # Any positive dividend
            score += 6
        else:
            score += 0
    
    # Revenue Growth (0-14 points) - Growth quality
    revenue_growth = safe_float(stock_data.get('revenue_growth'))
    if revenue_growth is not None:
        if 0.05 <= revenue_growth <= 0.15:  # Moderate, sustainable growth
            score += 14
        elif 0.02 <= revenue_growth <= 0.20:  # Reasonable growth range
            score += 12
        elif revenue_growth >= 0.01:  # Any positive growth
            score += 9
        elif revenue_growth >= 0:
            score += 6
        else:
            score += 0
    
    # Analyst Rating (0-16 points) - Market confidence quality
    analyst_rating = stock_data.get('average_analyst_rating')
    if analyst_rating is not None and analyst_rating:
        if 'Strong Buy' in analyst_rating:
            score += 16
        elif 'Buy' in analyst_rating:
            score += 12
        elif 'Hold' in analyst_rating:
            score += 8
        elif 'Sell' in analyst_rating:
            score += 2
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
            "de_ratio": info.get("debtToEquity"),
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
