# app/routes/stocks.py
import json
from datetime import datetime
from fastapi import APIRouter, Query
from typing import Optional
from app.services.stock_fetcher import get_stocks, calculate_stock_score

router = APIRouter()

@router.get("/")
def root():
    return {"message": "Welcome to Stock Rec API"}

@router.get("/health")
def health_check():
    global last_ping_time
    last_ping_time = datetime.utcnow()
    print(f"✅ Health check ping at {last_ping_time} UTC")
    return {
        "status": "ok",
        "last_ping": last_ping_time.isoformat()
    }

@router.get("/stocks")
def get_all_stocks(limit: int = 100, strategy: str = "balanced"):
    try:
        with open("stocks.json", "r") as f:
            stocks_data = json.load(f)

        # Convert the dictionary to a list of stock objects with symbol included
        stocks = []
        for symbol, data in stocks_data.items():
            stock = {
                "symbol": symbol, 
                **data
            }
            stocks.append(stock)
        
        # Sort by the selected strategy score in descending order (highest scores first)
        score_field = f"{strategy}_score"
        stocks.sort(key=lambda x: x.get(score_field, 0), reverse=True)
        
        # Return only the top-scoring stocks up to the limit
        top_stocks = stocks[:limit]
        
        print(f"Returning {len(top_stocks)} top-scoring stocks (limited to {limit})")
        if top_stocks:
            scores = [stock.get(score_field, 0) for stock in top_stocks]
            print(f"Score range: {max(scores)} - {min(scores)}")
        
        return top_stocks
    except FileNotFoundError:
        print("stocks.json file not found")
        return {"error": "Stocks data not available"}
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return {"error": "Invalid stocks data format"}
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {"error": "Internal server error"}
