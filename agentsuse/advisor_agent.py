from agents import Agent, Runner, trace
from agents.tool import WebSearchTool
from agentsuse.portfolio_agent import portfolio_agent
from agentsuse.budget_agent import budget_agent
from agentsuse.news_agent import news_agent
from agentsuse.sentiment_agent import sentiment_agent
from agentsuse.strategy_agent import strategy_agent

async def advisor_agent(user_input: str):
    advisor_prompt = f"""
You are a personal financial advisor AI.

Your job is to:
1. Understand the user's question or concern.
2. Decide which internal agents to consult (e.g. Portfolio, Budget, News, Sentiment, Strategy).
3. Summarize their output into a single, helpful, and conversational reply.

Available agents:
- Portfolio Agent: Analyzes investment returns, volatility, and price trends.
- Budget Agent: Evaluates spending behavior and budget structure.
- Strategy Agent: Suggests long-term or tactical investment approaches.
- Sentiment Agent: Analyzes market mood or emotional bias around assets.
- News Agent: Retrieves top financial headlines.

You may call one or more agents depending on the question. For example:
- If the user asks about investment performance, call the Portfolio Agent.
- If the user mentions concerns about the market, include News and Sentiment Agents.
- If the user wants help with goals, budgeting, or strategy, include Strategy or Budget Agents.

The user asked: \"{user_input}\"

Use web search if necessary. Be concise, kind, and give clear next steps.
"""

    advisor = Agent(
        name="Advisor Agent",
        instructions="Act as a financial advisor AI by synthesizing results from other agents.",
        tools=[WebSearchTool()]
    )

    with trace("Advisor Agent Responding"):
        result = await Runner.run(advisor, advisor_prompt)

    return {
        "agent_used": "Advisor Agent",
        "report": result.final_output,
        "summary_table": "",
        "chart_base64": None
    }
