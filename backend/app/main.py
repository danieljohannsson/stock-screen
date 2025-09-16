# app/main.py

from app.services.stock_fetcher import get_stocks
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import stocks
from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # You can restrict this later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(stocks.router)

@app.on_event("startup")
def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(get_stocks, "interval", minutes=1) # every minute
    scheduler.start()
    print("⏰ Scheduler started!")
