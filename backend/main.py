# main.py

import os
import uvicorn
from app.services.stock_fetcher import get_stocks
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import stocks
from apscheduler.schedulers.background import BackgroundScheduler

app = FastAPI()

# Dynamic CORS origins based on environment
def get_allowed_origins():
    origins = [
        "http://localhost:5173",  # Local development
        "http://localhost:3000",  # Alternative local port
        "https://*.vercel.app",   # Vercel deployments
        "https://*.render.com",   # Render deployments
    ]
    
    # Add localhost variations for development
    if os.environ.get("ENVIRONMENT") != "production":
        origins.extend([
            "http://127.0.0.1:5173",
            "http://127.0.0.1:3000",
            "http://localhost:8000",
            "http://127.0.0.1:8000",
        ])
    
    return origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_allowed_origins(),
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
    # For development, use localhost; for production, use 0.0.0.0
    host = "127.0.0.1" if os.environ.get("ENVIRONMENT") != "production" else "0.0.0.0"
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host=host, port=port)
