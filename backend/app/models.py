from sqlalchemy import Column, String, Float, Integer, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base

class Stock(Base):
    __tablename__ = "stocks"

    symbol = Column(String(10), primary_key=True, index=True)
    name = Column(String(255))
    price = Column(Float)
    pe_ratio = Column(Float)
    ps_ratio = Column(Float)
    pb_ratio = Column(Float)
    peg_ratio = Column(Float)
    roe = Column(Float)
    dividend_yield = Column(Float)
    free_cash_flow = Column(Float)
    revenue_growth = Column(Float)
    revenue_growth_3yr = Column(Float)
    earnings_growth = Column(Float)
    de_ratio = Column(Float)
    average_analyst_rating = Column(String(50))
    summary = Column(Text)
    industry = Column(String(255))
    website = Column(String(500))
    last_fetched = Column(DateTime(timezone=True), server_default=func.now())
    balanced_score = Column(Integer)
    value_score = Column(Integer)
    growth_score = Column(Integer)
    momentum_score = Column(Integer)
    quality_score = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class TickerProgress(Base):
    __tablename__ = "ticker_progress"

    id = Column(Integer, primary_key=True, index=True)
    last_index = Column(Integer, default=0)
    total_tickers = Column(Integer, default=0)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
