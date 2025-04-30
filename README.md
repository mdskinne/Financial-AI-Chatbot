# 💰 Financial AI Chatbot

An interactive, multi-agent financial assistant built with Python, Streamlit, and OpenAI function calling. This chatbot helps users analyze portfolios, budgets, market conditions, and financial strategies through specialized agents.

---

## 🚀 Features

- 📊 **Portfolio Agent**: Analyzes investment performance, trends, volatility, and generates graphs.
- 💵 **Budget Agent**: Breaks down expenses and tracks budget adherence.
- 💸 **Cashflow Agent**: Calculates monthly inflows/outflows and net cash flow.
- 📈 **Strategy Agent**: Suggests long- and short-term investment strategies.
- 🧾 **Tax Agent**: Answers investment-related tax questions.
- 💬 **QA Agent**: General-purpose financial Q&A.
- 🧠 **Education Agent**: Explains financial concepts clearly.
- 💹 **Sentiment Agent**: Analyzes market sentiment for stocks or sectors.
- 📉 **Live Pricing Agent**: Returns current prices for stocks and cryptocurrencies.
- 📰 **News Agent**: Summarizes recent financial headlines using live web search.
- 👔 **Advisor Agent**: Simulates a financial advisor by combining other agents' insights.

---

## 🧱 Architecture

- `manager_agent.py`: Routes user prompts to the correct AI agent using OpenAI function calling.
- Each agent is modular and uses shared formatting for consistent output.
- `app.py`: Streamlit frontend for interaction, visualization, and tracing agentic flows.
- Charts and tables are generated inline for portfolio and cash analysis.

---

## 🗂 Folder Structure
```
financechatbot/
├── app.py                  <- Streamlit frontend
├── manager_agent.py       <- Orchestrates agent routing
├── agentsuse/             <- Folder of all AI agent modules
│   ├── portfolio_agent.py
│   ├── budget_agent.py
│   ├── news_agent.py
│   └── ... (others)
├── sample_portfolio.csv   <- Portfolio input data
├── sample_budget.csv      <- Budget input data
```
## 🛠️ Setup

Install dependencies:
```
pip install -r requirements.txt
```
Set OpenAI API key:
```
export OPENAI_API_KEY="your-key"
```
Run the app:
```
streamlit run app.py
```
## 📌 Notes

All data (portfolio/budget) is hardcoded from sample CSVs. Upload your own data if necessary.

Live pricing and news use real-time tools (yfinance, WebSearchTool).





## 📜 License

MIT License

## ✨ Future Improvements

Add persistent memory

Goal Tracker or Net Worth agent

Natural language file upload (e.g., transaction logs)

