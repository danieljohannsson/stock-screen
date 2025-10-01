import os
import math
from pathlib import Path
import yfinance as yf
import pandas as pd
import json
from datetime import datetime
from dotenv import load_dotenv
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Stock, TickerProgress

load_dotenv()

BATCH_SIZE = 30

def calculate_stock_score(stock_data: Dict[str, Any], strategy: str = "balanced") -> int:
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

def _calculate_balanced_score(stock_data: Dict[str, Any], safe_float) -> int:
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
    
    return min(100, int(math.ceil(score)))

def _calculate_value_score(stock_data: Dict[str, Any], safe_float) -> int:
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
    
    return min(100, int(math.ceil(score)))

def _calculate_growth_score(stock_data: Dict[str, Any], safe_float) -> int:
    """Growth investing strategy with binary pass/fail criteria"""
    score = 0.0
    
    # 3-Year Revenue Growth (25 points) - Must be >20%
    revenue_growth_3yr = safe_float(stock_data.get('revenue_growth_3yr'))
    if revenue_growth_3yr is not None and revenue_growth_3yr > 0.20:
        score += 25
    
    # Revenue Growth YoY (25 points) - Must be ≥20%
    revenue_growth = safe_float(stock_data.get('revenue_growth'))
    if revenue_growth is not None and revenue_growth >= 0.20:
        score += 25
    
    # D/E Ratio (25 points) - Must be between 0 and 5
    de_ratio = safe_float(stock_data.get('de_ratio'))
    if de_ratio is not None and 0 <= de_ratio <= 5:
        score += 25
    
    # PEG Ratio (25 points) - Must be between 0 and 2
    peg_ratio = safe_float(stock_data.get('peg_ratio'))
    if peg_ratio is not None and 0 < peg_ratio <= 2:
        score += 25
    
    return min(100, int(math.ceil(score)))

def _calculate_momentum_score(stock_data: Dict[str, Any], safe_float) -> int:
    """Momentum investing strategy with binary pass/fail criteria"""
    score = 0.0
    
    # 3-Year Revenue Growth (20 points) - Must be >10%
    revenue_growth_3yr = safe_float(stock_data.get('revenue_growth_3yr'))
    if revenue_growth_3yr is not None and revenue_growth_3yr > 0.10:
        score += 20
    
    # Earnings Growth (20 points) - Must be >15%
    earnings_growth = safe_float(stock_data.get('earnings_growth'))
    if earnings_growth is not None and earnings_growth > 0.15:
        score += 20
    
    # Revenue Growth YoY (20 points) - Must be >20%
    revenue_growth = safe_float(stock_data.get('revenue_growth'))
    if revenue_growth is not None and revenue_growth > 0.20:
        score += 20
    
    # Return on Equity (20 points) - Must be >20%
    roe = safe_float(stock_data.get('roe'))
    if roe is not None and roe > 0.20:
        score += 20
    
    # Accelerating Revenue Growth (20 points) - YoY growth must be higher than 3-year growth
    if (revenue_growth is not None and revenue_growth_3yr is not None and 
        revenue_growth > revenue_growth_3yr):
        score += 20
    
    return min(100, int(math.ceil(score)))

def _calculate_quality_score(stock_data: Dict[str, Any], safe_float) -> int:
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
    
    return min(100, int(math.ceil(score)))

def fetch_info(ticker: str):
    try:
        return yf.Ticker(ticker).info
    except Exception as e:
        print(f"Error fetching quote for {ticker}: {e}")
        return {}

def calculate_3yr_revenue_growth(ticker: str) -> float:
    """
    Calculate 3-year annualized revenue growth rate from historical financial data.
    Returns the annualized growth rate as a decimal (e.g., 0.15 for 15%).
    """
    try:
        yf_ticker = yf.Ticker(ticker)
        financials = yf_ticker.financials
        
        if 'Total Revenue' not in financials.index:
            return None
            
        revenue_data = financials.loc['Total Revenue']
        
        # Need at least 2 years of data to calculate growth
        if len(revenue_data) < 2:
            return None
            
        # For 3-year growth, we want the most recent 4 years of data
        # Take the first 4 years if available, otherwise use all available data
        years_to_use = min(4, len(revenue_data))
        recent_data = revenue_data.iloc[:years_to_use]
        
        # Get the most recent and oldest revenue data from our selection
        latest_revenue = recent_data.iloc[0]  # Most recent
        oldest_revenue = recent_data.iloc[-1]  # Oldest in our selection
        
        # Check for valid data
        if latest_revenue <= 0 or oldest_revenue <= 0:
            return None
            
        # Calculate annualized growth rate
        years = len(recent_data) - 1
        annualized_growth = ((latest_revenue / oldest_revenue) ** (1/years)) - 1
        
        # Convert numpy types to Python float to avoid database issues
        return float(annualized_growth) if not pd.isna(annualized_growth) else None
        
    except Exception as e:
        print(f"Error calculating 3-year revenue growth for {ticker}: {e}")
        return None

def get_tickers_from_json() -> List[str]:
    """Load tickers from the existing JSON file"""
    ticker_file = "tickers_nyse.json"
    try:
        with open(ticker_file, "r") as f:
            ticker_data = json.load(f)
            # Handle both list format and dict format
            if isinstance(ticker_data, list):
                return ticker_data
            elif isinstance(ticker_data, dict):
                return ticker_data.get('tickers', [])
            else:
                print(f"Unexpected ticker file format: {type(ticker_data)}")
                return []
    except FileNotFoundError:
        print(f"Ticker file {ticker_file} not found")
        return []

def get_or_create_progress(db: Session) -> TickerProgress:
    """Get or create ticker progress record"""
    progress = db.query(TickerProgress).first()
    if not progress:
        progress = TickerProgress(last_index=0, total_tickers=0)
        db.add(progress)
        db.commit()
        db.refresh(progress)
    return progress

def save_stock_to_db(db: Session, symbol: str, metrics: Dict[str, Any]):
    """Save or update stock data in the database"""
    # Check if stock already exists
    existing_stock = db.query(Stock).filter(Stock.symbol == symbol).first()
    
    if existing_stock:
        # Update existing stock
        for key, value in metrics.items():
            if hasattr(existing_stock, key):
                setattr(existing_stock, key, value)
        existing_stock.last_fetched = datetime.utcnow()
    else:
        # Create new stock
        stock = Stock(symbol=symbol, **metrics)
        db.add(stock)
    
    db.commit()

def get_stocks():
    """Main function to fetch and save stock data"""
    db = SessionLocal()
    
    try:
        # Get tickers from JSON file
        all_tickers = get_tickers_from_json()
        if not all_tickers:
            print("No tickers found in JSON file")
            return []
        
        # Get or create progress tracking
        progress = get_or_create_progress(db)
        
        # Initialize total tickers if not set
        if progress.total_tickers == 0:
            progress.total_tickers = len(all_tickers)
            db.commit()
        
        # Get current batch
        index = progress.last_index
        batch = all_tickers[index:index + BATCH_SIZE]
        real_batch_size = len(batch)
        
        if real_batch_size < BATCH_SIZE:
            remaining = BATCH_SIZE - real_batch_size
            batch += all_tickers[:remaining]
        
        print(f"Processing batch starting at index {index}, processing {len(batch)} tickers")
        
        for symbol in batch:
            info = fetch_info(symbol)
            print(f"Fetched info for {symbol}")
            
            # Calculate 3-year revenue growth
            revenue_growth_3yr = calculate_3yr_revenue_growth(symbol)
            
            metrics = {
                "name": info.get("shortName") if info.get("shortName") else info.get("displayName"),
                "price": info.get("currentPrice"),
                "pe_ratio": info.get("trailingPE"),
                "ps_ratio": info.get("priceToSalesTrailing12Months"),
                "pb_ratio": info.get("priceToBook"),
                "peg_ratio": info.get("trailingPegRatio"),
                "roe": info.get("returnOnEquity"),
                "dividend_yield": info.get("dividendYield"),
                "free_cash_flow": info.get("freeCashflow"),
                "revenue_growth": info.get("revenueGrowth"),
                "revenue_growth_3yr": revenue_growth_3yr,
                "earnings_growth": info.get("earningsGrowth"),
                "de_ratio": info.get("debtToEquity") / 100 if info.get("debtToEquity") else None,
                "average_analyst_rating": info.get("averageAnalystRating").split(" - ")[1] if info.get("averageAnalystRating") else None,
                "summary": info.get("longBusinessSummary"),
                "industry": info.get("industry"),
                "website": info.get("website"),
                "last_fetched": datetime.utcnow(),
            }
            
            # Calculate and add scores
            metrics["balanced_score"] = calculate_stock_score(metrics, "balanced")
            metrics["value_score"] = calculate_stock_score(metrics, "value")
            metrics["growth_score"] = calculate_stock_score(metrics, "growth")
            metrics["momentum_score"] = calculate_stock_score(metrics, "momentum")
            metrics["quality_score"] = calculate_stock_score(metrics, "quality")
            
            # Save to database
            save_stock_to_db(db, symbol, metrics)
        
        # Update progress
        if real_batch_size < BATCH_SIZE:
            progress.last_index = remaining
        else:
            progress.last_index = index + BATCH_SIZE
        
        db.commit()
        
        print(f"✅ Saved {len(batch)} stocks to database")
        print(f"Progress: {progress.last_index}/{progress.total_tickers} tickers processed")
        
        return []
        
    except Exception as e:
        print(f"Error in get_stocks: {e}")
        db.rollback()
        return []
    finally:
        db.close()

def get_stocks_from_db(db: Session, limit: int = 100, strategy: str = "balanced") -> List[Dict]:
    """Get stocks from database sorted by strategy score"""
    score_column = getattr(Stock, f"{strategy}_score")
    
    stocks = db.query(Stock).order_by(score_column.desc()).limit(limit).all()
    
    result = []
    for stock in stocks:
        stock_dict = {
            "symbol": stock.symbol,
            "name": stock.name,
            "price": stock.price,
            "pe_ratio": stock.pe_ratio,
            "ps_ratio": stock.ps_ratio,
            "pb_ratio": stock.pb_ratio,
            "peg_ratio": stock.peg_ratio,
            "roe": stock.roe,
            "dividend_yield": stock.dividend_yield,
            "free_cash_flow": stock.free_cash_flow,
            "revenue_growth": stock.revenue_growth,
            "revenue_growth_3yr": stock.revenue_growth_3yr,
            "earnings_growth": stock.earnings_growth,
            "de_ratio": stock.de_ratio,
            "average_analyst_rating": stock.average_analyst_rating,
            "summary": stock.summary,
            "industry": stock.industry,
            "website": stock.website,
            "last_fetched": stock.last_fetched.isoformat() if stock.last_fetched else None,
            "balanced_score": stock.balanced_score,
            "value_score": stock.value_score,
            "growth_score": stock.growth_score,
            "momentum_score": stock.momentum_score,
            "quality_score": stock.quality_score,
        }
        result.append(stock_dict)
    
    return result