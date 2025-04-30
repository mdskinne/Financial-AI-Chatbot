import pandas as pd
import os

# 🔒 Path to your user-defined CSV (this file should not be edited by code)
CSV_PATH = "C:/Users/mdskinne/financechatbot/sample_budget.csv"

# 🔒 Load the CSV into memory once at import
try:
    _budget_df = pd.read_csv(CSV_PATH)
    _budget_df.columns = [col.strip().title() for col in _budget_df.columns]
    _budget_df["Date"] = pd.to_datetime(_budget_df["Date"], errors="coerce")
    _budget_df["Amount"] = pd.to_numeric(_budget_df["Amount"], errors="coerce").fillna(0)
    _budget_df = _budget_df.dropna(subset=["Date", "Amount"])
    print(f"✅ Budget data loaded from {CSV_PATH}")
except Exception as e:
    _budget_df = pd.DataFrame()
    print(f"❌ Failed to load budget CSV from {CSV_PATH}: {e}")

# ✅ Only expose a safe read-only accessor
def get_budget_df() -> pd.DataFrame:
    return _budget_df.copy()
