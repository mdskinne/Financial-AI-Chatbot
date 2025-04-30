import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from io import BytesIO
import base64


def analyze_portfolio(portfolio_df: pd.DataFrame):
    performance_data = []
    plt.figure(figsize=(10, 6))

    for _, row in portfolio_df.iterrows():
        ticker = row["Ticker"]
        buy_date = pd.to_datetime(row["Buy Date"])
        buy_price = row["Buy Price"]
        shares = row["Shares"]

        data = yf.download(ticker, start=buy_date, progress=False)
        if data.empty:
            continue

        latest_close = data["Close"].iloc[-1]
        current_value = latest_close * shares
        return_percent = ((latest_close - buy_price) / buy_price) * 100

        performance_data.append({
            "Ticker": ticker,
            "Buy Date": buy_date.date(),
            "Buy Price": float(round(buy_price, 2)),
            "Shares": int(shares),
            "Latest Price": float(round(latest_close, 2)),
            "Current Value": float(round(current_value, 2)),
            "Return (%)": float(round(return_percent, 2))
        })

        data["Value"] = data["Close"] * shares
        plt.plot(data.index, data["Value"], label=ticker)

    plt.title("Portfolio Value Over Time")
    plt.xlabel("Date")
    plt.ylabel("Position Value ($)")
    plt.legend()
    plt.tight_layout()

    # Convert plot to base64
    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode("utf-8")
    plt.close()

    summary_df = pd.DataFrame(performance_data)
    summary_df = summary_df[["Ticker", "Buy Date", "Buy Price", "Shares", "Latest Price", "Current Value", "Return (%)"]]
    summary_df = summary_df.round(2)
    summary_text = summary_df.to_markdown(index=False)

    return image_base64, summary_text
