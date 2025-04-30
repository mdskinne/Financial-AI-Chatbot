from agents import Agent, Runner, trace
from agents.tool import WebSearchTool

async def tax_agent(user_input: str):
    prompt = f"""
You are a tax-smart investment assistant. Respond to the following tax-related question with educational, general advice:

"{user_input}"

Your response should include:
1. An overview of tax considerations related to the question
2. Examples or scenarios (e.g., capital gains vs. income tax, short-term vs. long-term gains)
3. Tips for legally reducing taxes using common strategies (e.g., Roth accounts, tax-loss harvesting, holding periods)
4. A reminder to consult a tax professional for personal advice

Keep it professional, informative, and U.S.-focused unless specified otherwise.
"""

    agent = Agent(
        name="Tax Planning Agent",
        instructions="Offer general tax-smart investing advice and insights.",
        tools=[WebSearchTool()]
    )

    with trace("Generating Tax Guidance"):
        result = await Runner.run(agent, prompt)

    return {
        "agent_used": "Tax Agent",
        "report":result.final_output,
        "summary_table": "",
        "chart_base64": None
    }
