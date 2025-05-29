from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
from typing import List, Dict
from datetime import datetime
import yfinance as yf

app = FastAPI()

VALID_PERIODS = {"1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"}
VALID_INTERVALS = {"1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"}

class StockQuery(BaseModel):
    tickers: List[str]
    period: str = "1d"
    interval: str = "1h"

    @validator('period')
    def validate_period(cls, v):
        if v not in VALID_PERIODS:
            raise ValueError(f"Invalid period: {v}. Must be one of {VALID_PERIODS}")
        return v

    @validator('interval')
    def validate_interval(cls, v):
        if v not in VALID_INTERVALS:
            raise ValueError(f"Invalid interval: {v}. Must be one of {VALID_INTERVALS}")
        return v

@app.post("/get_stock_data/")
def get_stock_data(query: StockQuery) -> Dict:
    results = {}
    for ticker in query.tickers:
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period=query.period, interval=query.interval)
            info = stock.info

            price = hist['Close'].iloc[-1].item() if not hist.empty else None
            volume = hist['Volume'].iloc[-1].item() if not hist.empty else None

            if price is None or volume is None:
                results[ticker] = {
                    "error": f"No historical data available for {ticker}",
                    "currency": info.get("currency", "N/A"),
                    "shortName": info.get("shortName", "N/A"),
                    "sector": info.get("sector", "N/A")
                }
            else:
                results[ticker] = {
                    "price": price,
                    "volume": volume,
                    "currency": info.get("currency", "N/A"),
                    "shortName": info.get("shortName", "N/A"),
                    "sector": info.get("sector", "N/A")
                }
        except Exception as e:
            results[ticker] = {"error": str(e)}

    return {"timestamp": datetime.now().isoformat(), "data": results}
