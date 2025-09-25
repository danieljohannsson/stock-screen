# app/main.py

import os
from app.services.stock_fetcher import get_stocks
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import stocks
from apscheduler.schedulers.background import BackgroundScheduler

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Local development
        "https://*.vercel.app",   # Vercel deployments
        "https://*.render.com",   # Render deployments
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(stocks.router)

@app.on_event("startup")
def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(get_stocks, "interval", minutes=0.5) # every 30 seconds
    scheduler.start()
    print("⏰ Scheduler started!")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
