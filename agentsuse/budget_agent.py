import pandas as pd
from agents import Agent, Runner, trace
from agents.tool import WebSearchTool  # Optional if you want context-aware help
from budget_data_store import get_budget_df  # Custom data store function

async def budget_agent(user_input: str):
    query = user_input.strip().lower()

    df = get_budget_df()

    if df is None or df.empty:
        return "❌ No budget data found. Please upload your spending history first."

    # Ensure "Date" is in datetime format
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")

    prompt = f"""
    You are a personal finance AI agent. The user is asking the following question about their spending:
    
    👉 "{query}"

    Use the budget data below to answer their question with context and clarity. You may use numbers. Your answer should include:

    1. **Spending Summary**: Monthly or recent totals
    2. **Top Spending Categories**: Mention the largest areas of expense
    3. **Trends**: Any increasing or decreasing trends
    4. **Savings Insight**: Suggest where they may be able to save
    5. **Budget Adherence**: If budget categories are overspending, mention them
    6. **Closing Advice**: Wrap with a smart personal finance insight

    Budget data:
    {df.tail(300).to_string(index=False)}
    """

    agent = Agent(
        name="Budget Agent",
        instructions="Analyze personal budget and spending behavior from a given dataset.",
        tools=[WebSearchTool()]  # You can remove or replace with financial calculators/tools
    )

    with trace("Generating Budget Analysis"):
        result = await Runner.run(agent, prompt)

    return {
        "agent_used": "Budget Agent",
        "report": result.final_output,
        "summary_table": "",
        "chart_base64": None
    }