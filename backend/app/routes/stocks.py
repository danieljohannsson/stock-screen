from datetime import datetime
from fastapi import APIRouter, Query, Depends
from typing import Optional
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.stock_fetcher import get_stocks_from_db, calculate_stock_score

router = APIRouter()

@router.get("/")
def root():
    return {"message": "Welcome to Stock Rec API"}

@router.api_route("/health", methods=["GET", "HEAD"])
def health_check():
    global last_ping_time
    last_ping_time = datetime.utcnow()
    print(f"✅ Health check ping at {last_ping_time} UTC")
    return {
        "status": "ok",
        "last_ping": last_ping_time.isoformat()
    }

@router.get("/stocks")
def get_all_stocks(
    limit: int = 100, 
    strategy: str = "balanced",
    db: Session = Depends(get_db)
):
    try:
        # Get stocks from database
        stocks = get_stocks_from_db(db, limit=limit, strategy=strategy)
        
        print(f"Returning {len(stocks)} top-scoring stocks (limited to {limit})")
        if stocks:
            score_field = f"{strategy}_score"
            scores = [stock.get(score_field, 0) for stock in stocks if stock.get(score_field) is not None]
            if scores:
                print(f"Score range: {max(scores)} - {min(scores)}")
        
        return stocks
        
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {"error": "Internal server error"}