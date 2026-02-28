import uuid
import requests
import streamlit as st

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Agent",
    page_icon="🤖",
    layout="centered",
)

API_URL = "http://127.0.0.1:8000/chat"

# ── Session state ─────────────────────────────────────────────────────────────
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []   # list of {"role": "user"|"assistant", "content": str}

# ── Header ────────────────────────────────────────────────────────────────────
st.title("🤖 AI Agent")
st.caption("Powered by LangGraph + Groq · searches the web in real time")

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Session")
    st.code(st.session_state.session_id, language=None)
    if st.button("🗑️ Clear conversation"):
        st.session_state.messages = []
        st.session_state.session_id = str(uuid.uuid4())
        st.rerun()

    st.divider()
    st.markdown("**Backend:** `http://127.0.0.1:8000`")
    try:
        health = requests.get("http://127.0.0.1:8000/health", timeout=2)
        if health.ok:
            st.success("Backend online ✅")
        else:
            st.error("Backend returned an error")
    except Exception:
        st.error("Backend offline ❌")

# ── Chat history ──────────────────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── Input ─────────────────────────────────────────────────────────────────────
if prompt := st.chat_input("Ask me anything…"):
    # Show user message immediately
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call the FastAPI backend
    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            try:
                resp = requests.post(
                    API_URL,
                    json={"query": prompt, "session_id": st.session_state.session_id},
                    timeout=60,
                )
                resp.raise_for_status()
                answer = resp.json()["response"]
            except requests.exceptions.ConnectionError:
                answer = "❌ Could not reach the backend. Make sure the FastAPI server is running (`uvicorn app.agent.main:app --reload`)."
            except requests.exceptions.Timeout:
                answer = "⏱️ The request timed out. The agent may still be thinking — try again."
            except Exception as e:
                answer = f"❌ Unexpected error: {e}"

        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
