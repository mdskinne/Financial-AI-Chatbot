import openai
import json
import asyncio

from agentsuse.portfolio_agent import portfolio_agent
from agentsuse.budget_agent import budget_agent
from agentsuse.cashflow_agent import cashflow_agent
from agentsuse.strategy_agent import strategy_agent
from agentsuse.tax_agent import tax_agent
from agentsuse.sentiment_agent import sentiment_agent
from agentsuse.education_agent import education_agent
from agentsuse.qa_agent import qa_agent
from agentsuse.live_pricing_agent import live_pricing_agent
from agentsuse.news_agent import news_agent
from agentsuse.advisor_agent import advisor_agent

class ManagerAgent:
    def __init__(self):
        self.tools = self.define_tools()

    def define_tools(self):
        return [
            {
                "type": "function",
                "function": {
                    "name": "portfolio_agent",
                    "description": "Analyze the user's investment portfolio, including returns, risk, performance trends, and a summary report.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "A user query related to their portfolio, like performance, trends, or holdings."
                            }
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "budget_agent",
                    "description": "Review and analyze user budget and spending behavior.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The user question related to budget or expenses."
                            }
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "cashflow_agent",
                    "description": "Evaluate user's monthly or yearly cash flow and financial balance.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The user's question about cash inflow/outflow or surplus/deficit."
                            }
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "strategy_agent",
                    "description": "Provide investment strategy recommendations based on goals and risk.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The user's question about investment strategy."
                            }
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "tax_agent",
                    "description": "Answer tax-related questions for investments, income, or capital gains.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The user's question about taxes."
                            }
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "sentiment_agent",
                    "description": "Analyze market sentiment for a specific asset or sector.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Asset or keyword to analyze market sentiment."
                            }
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "education_agent",
                    "description": "Explain financial concepts in a simple and educational way.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The user's question about financial concepts or definitions."
                            }
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "qa_agent",
                    "description": "General financial Q&A about markets, investing, tools, or terminology. Also a fallback agent.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The user's general finance-related question."
                            }
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "live_pricing_agent",
                    "description": "Fetch the latest market price for a stock or crypto asset.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The ticker or symbol to fetch pricing for (e.g., AAPL, BTC-USD)."
                            }
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "news_agent",
                    "description": "Fetch and summarize recent financial news for a stock, company, or keyword.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Ticker symbol or search keyword (e.g. AAPL, inflation, interest rates)"
                            }
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "advisor_agent",
                    "description": "Provide financial advice by coordinating insights from multiple agents.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The user's question or financial concern."
                            }
                        },
                        "required": ["query"]
                    }
                }
            }
        ]

    async def handle_request(self, user_input: str):
        # 1. Try OpenAI function calling to determine the best agent
        response = await asyncio.to_thread(
            openai.chat.completions.create,
            model="gpt-4-1106-preview",
            messages=[
                {"role": "system", "content": "You are an assistant that routes financial analysis requests to specialized agents."},
                {"role": "user", "content": user_input}
            ],
            tools=self.tools,
            tool_choice="auto"
        )

        tool_calls = response.choices[0].message.tool_calls

        # 2. If OpenAI selects a tool, parse it
        if tool_calls:
            tool_call = tool_calls[0]
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            query = arguments.get("query", user_input)

            print(f"📡 Routed to: {tool_name}")
            return await self.route_to_agent(tool_name, query)

         #3. Fallback keyword-based routing if function call fails
        user_lower = user_input.lower()
        if "portfolio" in user_lower or "investment" in user_lower or "stock" in user_lower:
            print("🔁 Fallback to portfolio_agent based on keyword match.")
            return await self.route_to_agent("portfolio_agent", user_input)

        if "budget" in user_lower or "spending" in user_lower:
            print("🔁 Fallback to budget_agent based on keyword match.")
            return await self.route_to_agent("budget_agent", user_input)

        if "cash flow" in user_lower or "inflow" in user_lower or "outflow" in user_lower:
            print("🔁 Fallback to cashflow_agent based on keyword match.")
            return await self.route_to_agent("cashflow_agent", user_input)

        if "strategy" in user_lower or "invest" in user_lower:
            print("🔁 Fallback to strategy_agent based on keyword match.")
            return await self.route_to_agent("strategy_agent", user_input)

        if "tax" in user_lower:
            print("🔁 Fallback to tax_agent based on keyword match.")
            return await self.route_to_agent("tax_agent", user_input)

        if "define" in user_lower or "explain" in user_lower or "what is" in user_lower:
            print("🔁 Fallback to education_agent based on keyword match.")
            return await self.route_to_agent("education_agent", user_input)

        print("❌ No matching agent found.")
        return "🤖 Sorry, I couldn’t determine which agent to use for that request."

    
    async def route_to_agent(self, tool_name: str, query: str):
        if tool_name == "portfolio_agent":
            return await portfolio_agent(query)
        elif tool_name == "budget_agent":
            return await budget_agent(query)
        elif tool_name == "cashflow_agent":
            return await cashflow_agent(query)
        elif tool_name == "strategy_agent":
            return await strategy_agent(query)
        elif tool_name == "tax_agent":
            return await tax_agent(query)
        elif tool_name == "sentiment_agent":
            return await sentiment_agent(query)
        elif tool_name == "qa_agent":
            return await qa_agent(query)
        elif tool_name == "education_agent":
            return await education_agent(query)
        elif tool_name == "live_pricing_agent":
            return await live_pricing_agent(query)
        elif tool_name == "news_agent":
            return await news_agent(query)
        elif tool_name == "advisor_agent":
            return await advisor_agent(query)
        else:
            return {
                "agent_used": "Unknown",
                "report": f"❌ Unknown agent: {tool_name}",
                "summary_table": "",
                "chart_base64": None
            }
