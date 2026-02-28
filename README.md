# 🤖 AI Agent

A real-time AI assistant that searches the web to answer questions, built with **LangGraph**, **Groq (LLaMA 3.3 70B)**, and **FastAPI**, with a **Streamlit** chat frontend.

---

## ✨ Features

- 💬 ChatGPT-style chat interface
- 🔍 Real-time web search via DuckDuckGo
- 🧠 Per-session conversation memory
- ⚡ Fast inference using Groq's LLaMA 3.3 70B model
- 🔗 REST API backend (FastAPI) + interactive UI (Streamlit)

---

## 🏗️ Architecture

```
User (Streamlit UI)
        ↓  HTTP POST /chat
FastAPI Backend (uvicorn)
        ↓
LangGraph ReAct Agent
        ↓              ↓
  Groq LLM       DuckDuckGo Search
  (LLaMA 3.3)     (web_search tool)
```

---

## 📁 Project Structure

```
AI-Agent/
├── app/
│   └── agent/
│       ├── agent.py      # LangGraph ReAct agent + Groq LLM
│       ├── main.py       # FastAPI app & endpoints
│       ├── memory.py     # Conversation memory
│       └── tools.py      # DuckDuckGo web search tool
├── frontend.py           # Streamlit chat UI
├── requirements.txt
├── .env                  # API keys (not committed)
└── .gitignore
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/g-akshaya/AI-AGENT.git
cd AI-AGENT
```

### 2. Create a virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate       # Windows
# source .venv/bin/activate  # macOS/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Get a free API key at [console.groq.com](https://console.groq.com).

---

## ▶️ Running the App

You need **two terminals** — one for the backend, one for the frontend.

### Terminal 1 — FastAPI backend

```bash
python -m uvicorn app.agent.main:app --reload
```

Backend runs at `http://127.0.0.1:8000`

### Terminal 2 — Streamlit frontend

```bash
streamlit run frontend.py
```

Frontend runs at `http://localhost:8501`

---

## 🔌 API Reference

### `GET /health`
Returns server status.

```json
{ "status": "ok" }
```

### `POST /chat`
Send a message to the agent.

**Request:**
```json
{
  "query": "What happened in the news today?",
  "session_id": "user-123"
}
```

**Response:**
```json
{
  "response": "...",
  "session_id": "user-123"
}
```

Interactive docs available at `http://127.0.0.1:8000/docs`.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| LLM | Groq — LLaMA 3.3 70B Versatile |
| Agent framework | LangGraph (ReAct agent) |
| Web search | DuckDuckGo (`langchain-community`) |
| Backend | FastAPI + Uvicorn |
| Frontend | Streamlit |
| Memory | LangGraph `MemorySaver` (in-memory, per session) |
