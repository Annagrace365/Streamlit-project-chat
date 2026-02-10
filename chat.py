import streamlit as st
from groq import Groq
import os

# -------------------------------
# CONFIG
# -------------------------------
st.set_page_config(page_title="Groq Chat App", page_icon="🤖")

# Set your Groq API key (recommended via environment variable)
# export GROQ_API_KEY="your_key_here"
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# -------------------------------
# SESSION STATE (Conversation Memory)
# -------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful AI assistant."}
    ]

# -------------------------------
# UI
# -------------------------------
st.title("🤖 Groq Chat Application")
st.caption("Fast LLMs powered by Groq | Conversation Memory Enabled")

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# -------------------------------
# USER INPUT
# -------------------------------
user_prompt = st.chat_input("Ask something...")

if user_prompt:
    # Show user message
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Save user message to memory
    st.session_state.messages.append(
        {"role": "user", "content": user_prompt}
    )

    # -------------------------------
    # GROQ CHAT COMPLETION
    # -------------------------------
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=st.session_state.messages
    )

    assistant_reply = response.choices[0].message.content

    # Show assistant message
    with st.chat_message("assistant"):
        st.markdown(assistant_reply)

    # Save assistant reply to memory
    st.session_state.messages.append(
        {"role": "assistant", "content": assistant_reply}
    )
