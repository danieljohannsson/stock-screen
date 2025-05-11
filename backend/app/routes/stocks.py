# app/routes/stocks.py

from fastapi import APIRouter
from app.services.stock_fetcher import get_stocks

router = APIRouter()


@router.get("/stocks")
def list_stocks(symbol: str):
    results = get_stocks([symbol.upper()])
    return results
