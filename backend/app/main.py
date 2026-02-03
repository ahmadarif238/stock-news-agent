from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from apscheduler.schedulers.background import BackgroundScheduler
from typing import List

from app.database import create_db_and_tables, get_session
from app.models import Ticker, NewsAlert
from app.services.agent import run_agent_cycle
from fastapi.middleware.cors import CORSMiddleware

# --- Background Task Setup ---
scheduler = BackgroundScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    create_db_and_tables()
    scheduler.add_job(run_agent_cycle, 'interval', minutes=10) # Run every 10 mins
    scheduler.start()
    run_agent_cycle() # Run once immediately on startup
    yield
    # Shutdown
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for now (dev), restrict for prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- API Endpoints ---

@app.get("/tickers", response_model=List[Ticker])
def get_tickers(session: Session = Depends(get_session)):
    return session.exec(select(Ticker)).all()

@app.post("/tickers", response_model=Ticker)
def add_ticker(ticker: Ticker, session: Session = Depends(get_session)):
    existing = session.exec(select(Ticker).where(Ticker.symbol == ticker.symbol)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Ticker already exists")
    session.add(ticker)
    session.commit()
    session.refresh(ticker)
    # Trigger a cycle? maybe async
    return ticker

@app.delete("/tickers/{ticker_id}")
def delete_ticker(ticker_id: int, session: Session = Depends(get_session)):
    ticker = session.get(Ticker, ticker_id)
    if not ticker:
        raise HTTPException(status_code=404, detail="Ticker not found")
    session.delete(ticker)
    session.commit()
    return {"ok": True}

@app.get("/alerts", response_model=List[NewsAlert])
def get_alerts(session: Session = Depends(get_session)):
    # Return latest 50 alerts
    return session.exec(select(NewsAlert).order_by(NewsAlert.created_at.desc()).limit(50)).all()
