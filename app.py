from PIL import Image
import base64
from io import BytesIO
import streamlit as st
import asyncio
from manager_agent import ManagerAgent
from dotenv import load_dotenv
load_dotenv()

# Page config
st.set_page_config(page_title="Financial AI Chatbot", layout="wide")
st.title("💼 Financial AI Chatbot")
st.write("Ask about your portfolio, budget, cash flow, taxes, strategy, and more.")

# Initialize state
if "manager" not in st.session_state:
    st.session_state.manager = ManagerAgent()
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []
if "trace_log" not in st.session_state:
    st.session_state.trace_log = []

# Input from user
user_input = st.text_input("💬 What would you like to know?", key="user_input")
response = None

# Submit logic
if st.button("Submit") and user_input:
    with st.spinner("🤖 Thinking..."):
        response = asyncio.run(st.session_state.manager.handle_request(user_input))

    if response:
        if isinstance(response, dict):
            agent_name = response.get("agent_used", "Unknown")
            st.session_state.chat_log.append({
                "question": user_input,
                "agent": agent_name,
                "answer": response.get("report", ""),
                "summary": response.get("summary_table", ""),
                "chart": response.get("chart_base64", None)
            })
        else:
            st.session_state.chat_log.append({
                "question": user_input,
                "agent": "unknown",
                "answer": response,
                "summary": "",
                "chart": None
            })

# Icon mapping
icon_map = {
    "Portfolio Agent": "📊",
    "Budget Agent": "💸",
    "Cashflow Agent": "💵",
    "Education Agent": "📚",
    "QA Agent": "❓",
    "Sentiment Agent": "📈📉",
    "Strategy Agent": "🧠",
    "Tax Agent": "🧾",
    "Unknown": "⚠️",
    "unknown": "⚠️"
}

# Sidebar trace
st.sidebar.title("🧠 Agentic Flow")
for entry in reversed(st.session_state.chat_log[-10:]):
    agent = entry.get("agent", "unknown")
    icon = icon_map.get(agent, "🤖")
    question = entry.get("question", "")
    st.sidebar.markdown(f"{icon} **{agent}** → {question}")

# Main content
st.subheader("🧾 Chat History")
for chat in reversed(st.session_state.chat_log[-5:]):
    st.markdown(f"**You**: {chat['question']}")
    st.caption(f"🤖 Agent: `{chat['agent']}`")
    st.markdown(chat["answer"])

    if chat["summary"]:
        st.subheader("📋 Summary Table")
        st.markdown(chat["summary"])

    if chat["chart"]:
        try:
            img_bytes = base64.b64decode(chat["chart"])
            img = Image.open(BytesIO(img_bytes))
            st.image(img, caption="📈 Portfolio Value Over Time", use_container_width=True)
        except Exception as e:
            st.error(f"❌ Failed to display chart: {e}")

    st.markdown("---")
