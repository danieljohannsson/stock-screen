# app/routes/stocks.py
import json
from fastapi import APIRouter, Query
from typing import Optional
from app.services.stock_fetcher import get_stocks

router = APIRouter()


@router.get("/stocks")
def get_all_stocks(limit: int = 100):
    try:
        with open("stocks.json", "r") as f:
            stocks_data = json.load(f)

        # Convert the dictionary to a list of stock objects with symbol included
        stocks = []
        count = 0
        for symbol, data in stocks_data.items():
            if count >= limit:
                break
            stock = {"symbol": symbol, **data}
            stocks.append(stock)
            count += 1
        
        print(f"Returning {len(stocks)} stocks (limited to {limit})")
        return stocks
    except FileNotFoundError:
        print("stocks.json file not found")
        return {"error": "Stocks data not available"}
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return {"error": "Invalid stocks data format"}
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {"error": "Internal server error"}

@router.get("/search")
def search_stocks(
    symbol: Optional[str] = Query(default=None),
    industry: Optional[str] = Query(default=None),
    country: Optional[str] = Query(default="US")
):
    if symbol:
        stock_data = get_stocks([symbol.upper()])
        return stock_data
    else:
        return {"error": "Please provide a symbol or industry."}
