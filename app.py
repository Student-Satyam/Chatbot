import streamlit as st
import os
from openai import OpenAI

# Ensure the API key is set as an environment variable
# In a real-world scenario, you would manage this more securely, e.g., using Streamlit secrets
# For Colab, you used os.environ, for Streamlit locally, you might set it in your environment or .streamlit/secrets.toml
# For demonstration, we'll try to get it from environment, and prompt user if not found.

if "OPENAI_API_KEY" not in os.environ:
    st.warning("OPENAI_API_KEY environment variable not set. Please set it or use Streamlit secrets.")
    # As a fallback for demonstration, you can uncomment the line below and paste your key,
    # but it's not recommended for production.
    # os.environ["OPENAI_API_KEY"] = "your_openai_api_key_here"

client = OpenAI()

def ask_ai(text):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": text}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"

st.title("Simple AI Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What would you like to know?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get AI response
    with st.chat_message("assistant"):
        response = ask_ai(prompt)
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
