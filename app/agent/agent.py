import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

from app.agent.tools import tools

load_dotenv()

SYSTEM_PROMPT = (
    "You are a helpful AI assistant. "
    "When you need current or real-time information, use the available tools."
)

# --- LLM ---
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    groq_api_key=os.getenv("GROQ_API_KEY"),
)

# --- Agent with in-memory checkpointer for per-session memory ---
_checkpointer = MemorySaver()
_agent = create_react_agent(
    model=llm,
    tools=tools,
    checkpointer=_checkpointer,
)


def run_agent(query: str, session_id: str = "default") -> str:
    """Run the agent; memory is scoped per session_id via the checkpointer."""
    config = {"configurable": {"thread_id": session_id}}
    result = _agent.invoke(
        {"messages": [HumanMessage(content=query)]},
        config=config,
    )
    return result["messages"][-1].content
