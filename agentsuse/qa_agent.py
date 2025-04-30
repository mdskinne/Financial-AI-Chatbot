from agents import Agent, Runner, trace
from agents.tool import WebSearchTool

async def qa_agent(user_input: str):
    prompt = f"""
You are a highly intelligence financial assistant. Answer the following question clearly and accurately only if it relates to finance. If it does not relate to finance, respond with 'I am limited to financial questions.'

Question:
{user_input}

Your response should include:
- A concise but complete answer
- Examples if helpful
- A friendly, professional tone
- No financial advice disclaimers unless legally necessary
"""

    agent = Agent(
        name="Finance Q&A Agent",
        instructions="Answer general finance and investment-related questions with clarity and accuracy.",
        tools=[WebSearchTool()],
    )

    with trace("General Finance QA"):
        result = await Runner.run(agent, prompt)

    return {
        "agent_used": "QA Agent",
        "report": result.final_output,
        "summary_table": "",
        "chart_base64": None
    }