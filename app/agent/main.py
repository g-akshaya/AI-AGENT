from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.concurrency import run_in_threadpool

from app.agent.agent import run_agent

app = FastAPI(
    title="Live AI Assistant",
    description="An AI agent that can search the web, answer questions in real time, and verify answers using the latest data.",
    version="1.0.0",
)


# --- Request / Response schemas ---
class ChatRequest(BaseModel):
    query: str
    session_id: str = "default"  # Use different session IDs for separate conversations


class ChatResponse(BaseModel):
    response: str
    session_id: str


# --- Endpoints ---
@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Send a message to the AI assistant.
    The agent will search the web when needed to provide real-time, verified answers.
    """
    response = await run_in_threadpool(run_agent, request.query, request.session_id)
    return ChatResponse(response=response, session_id=request.session_id)
