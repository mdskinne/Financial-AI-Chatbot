import pandas as pd
from agents import Agent, Runner, trace
from agents.tool import WebSearchTool
from portfolio_data_store import get_portfolio_df
from analyze_portfolio import analyze_portfolio

async def portfolio_agent(user_input: str):
    # Load the full portfolio (ignoring ticker — your CSV holds all tickers now)
    df = get_portfolio_df()
    
    if df is None or df.empty:
        return "❌ No portfolio data found. Please check your CSV file."

    # Analyze portfolio: generates base64 chart and performance summary text
    image_base64, summary_text = analyze_portfolio(df)

    # Construct prompt with summary
    prompt = f"""
You are a financial analyst AI. Based on the portfolio performance summary below,
write a clear, professional report that includes:

1. An overview of the portfolio's total return
2. Calculate Returns
3. Best and worst performing positions
4. Patterns you notice in price/value behavior
5. Any risk indicators or volatility concerns
6. Recommendations for a long-term investor

Summary Table:
{summary_text}
"""

    # Define and run the agent
    agent = Agent(
        name="Portfolio Analysis Agent",
        instructions="Analyze portfolio performance from historical price data. Write a financial analysis report based on the portfolio summary.",
        tools=[WebSearchTool()]  # Optional: You can remove this if not used
    )

    with trace("Generating Portfolio Report"):
        result = await Runner.run(agent, prompt)

    # Return a structured response
    return {
        "agent_used": "Portfolio Agent",
        "report": result.final_output,
        "summary_table": summary_text,
        "chart_base64": image_base64
    }
