import pandas as pd
from agents import Agent, Runner, trace
from budget_data_store import get_budget_df

def infer_type(category: str) -> str:
    income_keywords = ["paycheck", "salary", "bonus", "freelance", "refund", "reimbursement", "income"]
    return "Income" if any(word in str(category).lower() for word in income_keywords) else "Expense"

async def cashflow_agent(user_input: str):
    df = get_budget_df()
    
    if df is None or df.empty:
        return "❌ No budget data available."

    df["Type"] = df["Category"].apply(infer_type)
    df["Month"] = df["Date"].dt.to_period("M")
    summary = df.groupby(["Month", "Type"])["Amount"].sum().unstack().fillna(0)
    summary["Net Cash Flow"] = summary.get("Income", 0) - summary.get("Expense", 0)

    summary_text = summary.round(2).to_string()

    prompt = f"""
You are a financial assistant. Analyze this monthly cash flow summary and explain:

1. Monthly surplus/deficit patterns
2. Average income, expenses, and savings rate
3. Any inconsistencies or warnings
4. Tips to improve the user’s cash flow

Cash Flow Summary:
{summary_text}
"""

    agent = Agent(
        name="Cash Flow Agent",
        instructions="Generate a cash flow report from the user's monthly net summary.",
        tools=[]
    )

    with trace("Generating Cash Flow Analysis"):
        result = await Runner.run(agent, prompt)

    return {
        "agent_used": "Cashflow Agent",
        "report": result.final_output,
        "summary_table": summary_text,
        "chart_base64": None
    }
