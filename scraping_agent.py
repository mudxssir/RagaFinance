from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Any
import yfinance as yf
import asyncio

app = FastAPI()

class EarningsRequest(BaseModel):
    tickers: List[str]

async def fetch_earnings(ticker: str) -> Dict[str, Any]:
    loop = asyncio.get_running_loop()
    try:
        stock = yf.Ticker(ticker)
        earnings = await loop.run_in_executor(None, lambda: stock.earnings)
        if earnings is not None and not earnings.empty:
            latest = earnings.iloc[-1].to_dict()
            return {ticker: {"earnings": latest}}
        else:
            return {ticker: {"error": "No earnings data available"}}
    except Exception as e:
        return {ticker: {"error": str(e)}}

@app.post("/get_earnings_surprises/")
async def get_earnings_surprises(request: EarningsRequest):
    tasks = [fetch_earnings(ticker) for ticker in request.tickers]
    results_list = await asyncio.gather(*tasks)
    results = {}
    for res in results_list:
        results.update(res)
    return results
