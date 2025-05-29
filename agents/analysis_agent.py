from typing import Dict, Any

def analyze_stock_data(stock_data: Dict[str, Any]) -> Dict[str, str]:
    """
    Example analysis function that:
    - Highlights price movements (up/down)
    - Summarizes earnings surprises if available
    - Combines into a simple summary text per ticker
    """

    analysis_results = {}

    for ticker, data in stock_data.items():
        if "error" in data:
            analysis_results[ticker] = f"Data error: {data['error']}"
            continue

        price = data.get("price")
        change_percent = data.get("change_percent")
        earnings_surprise = data.get("earnings_surprise")  # Optional, from scraping/earnings agent
        news_summary = data.get("news_summary")  # Optional

        summary_parts = []

        if price is not None and change_percent is not None:
            summary_parts.append(f"{ticker} closed at {price} USD, with a change of {change_percent}.")

        if earnings_surprise:
            summary_parts.append(f"Earnings surprise: {earnings_surprise}")

        if news_summary:
            summary_parts.append(f"Latest news: {news_summary}")

        if not summary_parts:
            summary_parts.append(f"No sufficient data available for {ticker}.")

        analysis_results[ticker] = " ".join(summary_parts)

    return analysis_results


# Quick local test
if __name__ == "__main__":
    sample_data = {
        "AAPL": {
            "price": 172.5,
            "change_percent": "+1.24%",
            "earnings_surprise": "Beat estimates by 3%",
            "news_summary": "Apple announced a new iPhone release."
        },
        "TSLA": {
            "price": 693.4,
            "change_percent": "-2.05%",
            "earnings_surprise": "Missed estimates by 1%",
            "news_summary": "Tesla faces production delays."
        }
    }

    analysis = analyze_stock_data(sample_data)
    for ticker, summary in analysis.items():
        print(f"{ticker} Analysis: {summary}")
