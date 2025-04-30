import pandas as pd
import os

# Updated path to your uploaded portfolio file
CSV_PATH = ".../sample_portfolio.csv"

try:
    _portfolio_df = pd.read_csv(CSV_PATH)
    _portfolio_df.columns = [col.strip().title() for col in _portfolio_df.columns]

    # Expect columns: Buy Date, Ticker, Buy Price, Shares
    _portfolio_df["Buy Date"] = pd.to_datetime(_portfolio_df["Buy Date"], errors="coerce")
    _portfolio_df["Buy Price"] = pd.to_numeric(_portfolio_df["Buy Price"], errors="coerce")
    _portfolio_df["Shares"] = pd.to_numeric(_portfolio_df["Shares"], errors="coerce")
    _portfolio_df = _portfolio_df.dropna(subset=["Buy Date", "Ticker", "Buy Price", "Shares"])

    print(f"✅ Portfolio CSV loaded from {CSV_PATH}")
except Exception as e:
    _portfolio_df = pd.DataFrame()
    print(f"❌ Failed to load portfolio CSV from {CSV_PATH}: {e}")

# Access full portfolio
def get_portfolio_df() -> pd.DataFrame:
    return _portfolio_df.copy()
