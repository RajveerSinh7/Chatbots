import os
import streamlit as st
from openai import OpenAI  # ✅ correct import

st.title("AI Chat Bot 🤖")

# Initialize OpenAI client using environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # ✅ you set this in terminal

# Set default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What’s up?"):
    # Show user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate assistant response (API CALL)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        # ✅ FIXED: use the client instance, not openai.ChatCompletion
        for chunk in client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            if chunk.choices[0].delta.get("content"):
                full_response += chunk.choices[0].delta.content
                message_placeholder.markdown(full_response + "▌")

        message_placeholder.markdown(full_response)

    # Save assistant response to session
    st.session_state.messages.append({"role": "assistant", "content": full_response})