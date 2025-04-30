from agents import Agent, Runner, trace
from agents.tool import WebSearchTool

async def news_agent(user_input: str):
    prompt = f"""
You are a financial news summarizer. Search for the latest and most relevant financial news related to the topic, company, or keyword: "{user_input}"

Your job is to:
1. Perform a web search using the tools provided.
2. Identify 3 to 5 relevant headlines from trusted sources (e.g. CNBC, Bloomberg, Yahoo Finance).
3. Summarize them clearly with title, source, and brief takeaway.

Return a clean, well-formatted list of headlines with links. For each item include:
- Title
- Brief takeaway
- Source (e.g., CNBC)
- A link to the article

"""

    agent = Agent(
        name="News Agent",
        instructions="Find and summarize the latest financial news using web search.",
        tools=[WebSearchTool()]
    )

    with trace("Fetching and Summarizing News"):
        result = await Runner.run(agent, prompt)

    return {
        "agent_used": "News Agent",
        "report": result.final_output,
        "summary_table": "",
        "chart_base64": None
    }
