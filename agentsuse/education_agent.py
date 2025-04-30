from agents import Agent, Runner, trace
from agents.tool import WebSearchTool

async def education_agent(user_input: str):
    prompt = f"""
You are a financial educator. Your job is to teach and explain financial and investing concepts clearly and thoroughly to beginners.nswer the following question clearly and accurately only if it relates to finance. If it does not relate to finance, respond with 'I am limited to financial questions.'

Please explain the following concept:
{user_input}

Your explanation should include:
- A beginner-friendly definition
- A real-world example or analogy
- A use-case or application
- If applicable, how it compares to similar concepts
- Keep it clear, friendly, and concise
"""

    agent = Agent(
        name="Education Agent",
        instructions="Explain financial and investment terms clearly, with examples and context.",
        tools=[WebSearchTool()]
    )

    with trace("Generating Educational Response"):
        result = await Runner.run(agent, prompt)

    return {
        "agent_used": "Education Agent",
        "report":result.final_output,
        "summary_table":"",
        "chart_base64": None
    }
