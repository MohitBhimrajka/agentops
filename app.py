# app.py

import streamlit as st
import vertexai
from vertexai import agent_engines

# --- Vertex AI Initialization ---
vertexai.init(
    project="agentops-dev",
    location="us-central1",
    staging_bucket="gs://mohit-adk"
)

# --- Deployed Agent Resource ---
RESOURCE_NAME = "projects/719580855933/locations/us-central1/reasoningEngines/803232826508967936"

@st.cache_resource
def get_remote_app():
    return agent_engines.get(resource_name=RESOURCE_NAME)

# --- Streamlit Layout ---
st.set_page_config(page_title="ADK Agent Chat", page_icon="🤖")
st.title("🤖 Chat with Your Deployed ADK Agent")
st.caption("Streaming queries through Vertex AI Agent Engine")

remote_app = get_remote_app()

# --- Session Management ---
if "session_id" not in st.session_state:
    session = remote_app.create_session(user_id="streamlit_user")
    st.session_state.session_id = session["id"]

session_id = st.session_state.session_id

# --- Chat History Management ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display history
for role, msg in st.session_state.chat_history:
    st.chat_message(role).write(msg)

# --- Input Box ---
user_input = st.chat_input("Type your message here...")

if user_input:
    # Show user input
    st.chat_message("user").write(user_input)
    st.session_state.chat_history.append(("user", user_input))

    # Assistant placeholder
    assistant_msg = st.chat_message("assistant")
    response_placeholder = assistant_msg.empty()
    full_response = ""

    # Debug log
    with st.expander("🔍 Agent Event Debug Log"):
        for event in remote_app.stream_query(
            user_id="streamlit_user",
            session_id=session_id,
            message=user_input
        ):
            # Show raw event
            st.json(event)

            # ✅ Safely extract model message
            if "content" in event and "parts" in event["content"]:
                parts = event["content"]["parts"]
                text = parts[0].get("text", "")
                full_response += text
                response_placeholder.markdown(full_response)

    st.session_state.chat_history.append(("assistant", full_response))
