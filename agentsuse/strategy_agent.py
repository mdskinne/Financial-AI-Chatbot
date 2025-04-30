from agents import Agent, Runner, trace
from agents.tool import WebSearchTool

async def strategy_agent(user_input: str):
    prompt = f"""
You are an investment strategy advisor AI. Respond to the following request with thoughtful guidance:

"{user_input}"

Your response should include:
1. A strategy tailored to a generic investor profile (long-term, diversified, risk-aware)
2. Asset classes or allocations that might be relevant
3. Pros and cons of the approach
4. Optional next steps or considerations (e.g., rebalancing, risk tolerance, goals)
5. Keep it professional, educational, and NOT personalized financial advice
"""

    agent = Agent(
        name="Investment Strategy Agent",
        instructions="Offer investment strategy insights tailored to generic user goals or prompts.",
        tools=[WebSearchTool()],
    )

    with trace("Generating Investment Strategy"):
        result = await Runner.run(agent, prompt)

    return {
        "agent_used": "Strategy Agent",
        "report":result.final_output,
        "summary_table": "",
        "chart_base64": None
    }