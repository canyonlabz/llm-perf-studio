import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import os

# Importing custom styles for the chatbot area
from src.ui.page_styles import inject_chatbot_area_styles
# Import OpenAI client
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

chatbot_prompt = """
You are an AI assistant specialized in performance testing. Help the user with JMeter scripts, load testing strategies, and performance analysis.
"""

# -- Page Chatbot Definitions -----------------------------------------------------------

def render_chatbot_area(llm_model="gpt-4o-mini"):
    """
    Render the interactive chatbot area for performance testing assistance.
    """
    # Inject custom CSS for styling
    inject_chatbot_area_styles()  # Apply custom styles for the chatbot area

    # Centered column for the chatbot
    col_left, col_chat, col_right = st.columns([2, 6, 2])

    with col_left:
        on = st.toggle(
            "Test Mode",
            value=False,
            key="enable_llm_mode",
            help="Toggle local LLM mode on or off.",)
        if on:
            st.markdown('<div class="chatbot-title">💬 LLM Mode Enabled</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="chatbot-title">🧪 Test Mode Enabled</div>', unsafe_allow_html=True)
        
    with col_chat:
        # --- Chatbot Section ---
        st.markdown('<div class="chatbot-title">🤖 Chatbot:</div>', unsafe_allow_html=True)

        # Initialize chat history in session state
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {"role": "system", "content": chatbot_prompt}
            ]

        # Create a container with fixed height for ALL chat content
        chat_container = st.container(height=320, border=True)

        # Get user input FIRST (before displaying messages)
        user_input = st.chat_input("Ask me about performance testing...")
        
        # Process any new user input
        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})

            # Show spinner while waiting for LLM response
            with st.spinner("Thinking..."):
                # Get AI response
                response = client.chat.completions.create(
                    model=llm_model,
                    messages=st.session_state.messages,
                    temperature=0.7,
                )
  
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response.choices[0].message.content})
       
        # Display ALL messages INSIDE the container
        with chat_container:
            # Display chat messages (excluding system prompt)
            for message in st.session_state.messages:
                if message["role"] != "system":
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])

    with col_right:
        st.button("🧹 Clear Chat", key="clear_chat", on_click=clear_chat)

# --- Callback function to clear chat ---
def clear_chat():
    """
    Clear the chat history in session state.
    """
    # Clear chat history
    st.session_state.chat_history = []
    st.session_state.messages = [
        {"role": "system", "content": chatbot_prompt}
    ]
