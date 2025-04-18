# 📁 tools/stock_tool.py
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta

def fetch_stock_data(company_name: str) -> dict:
    """Fetch stock data using company name, attempting to find the correct ticker"""
    try:
        # First try to find the ticker symbol from company name
        search_results = yf.Tickers(company_name).tickers
        if not search_results:
            return create_na_response("Company not found")
        
        # Use first result (most likely match)
        ticker = list(search_results.keys())[0]
        stock = search_results[ticker]
        
        info = stock.info
        if not info:
            return create_na_response("No stock info available")
            
        return {
            "symbol": ticker.upper(),
            "price": info.get("currentPrice", info.get("regularMarketPrice", "N/A")),
            "change": info.get("regularMarketChangePercent", "N/A"),
            "market_cap": info.get("marketCap", "N/A"),
            "valid": True  # Flag to indicate successful fetch
        }
    except Exception as e:
        print(f"[Stock Fetch Error] {e}")
        return create_na_response(str(e))

def create_na_response(reason: str) -> dict:
    """Helper to create consistent N/A responses"""
    return {
        "symbol": "N/A",
        "price": "N/A",
        "change": "N/A",
        "market_cap": "N/A",
        "valid": False,
        "error": reason
    }

def plot_stock_chart(ticker: str):
    try:
        end = datetime.today()
        start = end - timedelta(days=30)
        df = yf.download(ticker, start=start, end=end)

        if df.empty:
            raise ValueError("No data returned from yfinance.")

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name='Close'))

        fig.update_layout(
            title=f"{ticker.upper()} – 30-Day Stock Price Trend",
            xaxis_title="Date",
            yaxis_title="Price (USD)",
            template="plotly_white"
        )
        return fig
    except Exception as e:
        print(f"[Stock Chart Error] {e}")
        return None
