from agents import Agent, Runner, trace
from agents.tool import WebSearchTool

async def sentiment_agent(user_input: str):
    prompt = f"""
You are a sentiment analyst AI. Use recent headlines or search data to analyze the current investor or market sentiment around the following:

"{user_input}"

Your response should include:
1. A clear summary of the sentiment (positive, negative, mixed, uncertain)
2. A few reasons why this sentiment might exist (based on headlines or general perception)
3. How sentiment might influence investor behavior (buying/selling)
4. A professional and objective tone
"""

    agent = Agent(
        name="Sentiment Agent",
        instructions="Analyze sentiment based on search or market data. Return a brief sentiment report.",
        tools=[WebSearchTool()]
    )

    with trace("Generating Sentiment Report"):
        result = await Runner.run(agent, prompt)

    return {
        "agent_used": "Sentiment Agent",
        "report":result.final_output,
        "summary_table": "",
        "chart_base64": None
    }
