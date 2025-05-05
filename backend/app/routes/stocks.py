# app/routes/stocks.py

from fastapi import APIRouter
from app.services.stock_fetcher import get_undervalued_stocks

router = APIRouter()

@router.get("/stocks")
def list_undervalued_stocks():
    symbols = ["AAPL", "MSFT", "GOOGL", "F", "WFC", "BAC"]
    return get_undervalued_stocks(symbols)
