import os
import streamlit as st
import vertexai
from vertexai.preview import reasoning_engines

# --- Configuration ---
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "agentops-dev")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
ENGINE_RESOURCE = os.getenv(
    "VERTEX_AGENT_ENGINE",
    "projects/719580855933/locations/us-central1/reasoningEngines/803232826508967936"
)

# --- Initialize Vertex AI SDK ---
vertexai.init(project=PROJECT_ID, location=LOCATION)
agent_engine = reasoning_engines.ReasoningEngine(ENGINE_RESOURCE)

# --- Streamlit UI setup ---
st.set_page_config(page_title="AgentOps Chat", layout="wide")
st.title("🔎 AgentOps Chat Interface")
st.markdown("""
Welcome to your custom ADK-powered chatbot built with Google Vertex AI.

**Instructions:**
- Set your name using the sidebar.
- Ask any question using the chat box below.
- Clear the session anytime to restart the conversation.
""")

# --- Sidebar controls ---
st.sidebar.header("Settings")
user_name = st.sidebar.text_input("Your Name", value="Guest")

if st.sidebar.button("🧹 Clear Chat"):
    st.session_state.clear()
    st.experimental_rerun()

# --- Initialize message and session states ---
if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "session_id" not in st.session_state:
    import uuid
    st.session_state["session_id"] = f"session-{str(uuid.uuid4())}"

# --- Handle chat input ---
user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state["messages"].append({"author": user_name, "content": user_input})
    
    response = agent_engine.query(
        input=user_input,
        config={"configurable": {"session_id": st.session_state["session_id"]}}
    )
    
    st.session_state["messages"].append({"author": "Agent", "content": response.text})

# --- Display full conversation ---
for msg in st.session_state["messages"]:
    role = "user" if msg["author"] == user_name else "assistant"
    st.chat_message(role).write(msg["content"])
