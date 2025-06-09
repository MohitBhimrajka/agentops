import os
import uuid
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
    st.rerun()

# --- Initialize or retrieve the reasoning engine session ---
# This block will now also handle the user_id for the session.
if "reasoning_engine_session" not in st.session_state:
    # Generate a unique user ID once per browser session.
    if "user_id" not in st.session_state:
        st.session_state["user_id"] = f"st-user-{uuid.uuid4()}"

    # Connect to the deployed Reasoning Engine
    agent_engine = reasoning_engines.ReasoningEngine(ENGINE_RESOURCE)

    # Create a new session, now passing the required user_id
    st.session_state["reasoning_engine_session"] = agent_engine.create_session(
        user_id=st.session_state["user_id"]
    )

# Initialize message history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# --- Display existing chat messages ---
for msg in st.session_state["messages"]:
    role = "user" if msg["author"] == user_name else "assistant"
    with st.chat_message(role):
        st.write(msg["content"])

# --- Handle new chat input ---
if user_input := st.chat_input("Type your message..."):
    # Add user message to chat history and display it
    st.session_state["messages"].append({"author": user_name, "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Query the agent using the session object
    with st.spinner("Agent is thinking..."):
        session = st.session_state["reasoning_engine_session"]
        response = session.query(input=user_input)

    # Add agent response to chat history and display it
    agent_response_content = response.text
    st.session_state["messages"].append({"author": "Agent", "content": agent_response_content})
    with st.chat_message("assistant"):
        st.write(agent_response_content)