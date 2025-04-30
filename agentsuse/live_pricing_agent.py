import yfinance as yf
from agents import Agent, Runner, trace

async def live_pricing_agent(user_input: str):
    symbol = user_input.strip().upper()

    try:
        ticker = yf.Ticker(symbol)
        price_data = ticker.history(period="1d")

        if price_data.empty:
            return {
                "agent_used": "Live Pricing Agent",
                "report": f"❌ No live price found for {symbol}.",
                "summary_table": "",
                "chart_base64": None
            }

        latest_price = price_data["Close"].iloc[-1]
        previous_close = price_data["Close"].iloc[-2] if len(price_data) > 1 else latest_price
        change = latest_price - previous_close
        pct_change = (change / previous_close) * 100 if previous_close else 0

        report = f"""
📈 **{symbol} Live Price**
- Current Price: ${latest_price:,.2f}
- Change: ${change:,.2f} ({pct_change:.2f}%)
- Data as of: {price_data.index[-1].strftime('%Y-%m-%d %H:%M')}
"""

        return {
            "agent_used": "Live Pricing Agent",
            "report": report,
            "summary_table": "",
            "chart_base64": None
        }

    except Exception as e:
        return {
            "agent_used": "Live Pricing Agent",
            "report": f"❌ Error fetching data for {symbol}: {e}",
            "summary_table": "",
            "chart_base64": None
        }
