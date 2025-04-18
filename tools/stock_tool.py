# 📁 tools/stock_tool.py
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta

def fetch_stock_data(ticker: str) -> dict:
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return {
            "symbol": ticker.upper(),
            "price": info.get("currentPrice", "N/A"),
            "change": info.get("regularMarketChangePercent", "N/A"),
            "market_cap": info.get("marketCap", "N/A")
        }
    except Exception as e:
        print(f"[Stock Fetch Error] {e}")
        return {
            "symbol": "N/A",
            "price": "N/A",
            "change": "N/A",
            "market_cap": "N/A"
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