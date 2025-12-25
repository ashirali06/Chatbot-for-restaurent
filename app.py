import streamlit as st
from backend import ChatbotBackend
from admin import render_admin_panel
from data import DataManager

# Page Config
st.set_page_config(page_title="AI Restaurant Assistant", page_icon="🍽️", layout="wide")

# Initialize Backend
if "backend" not in st.session_state:
    st.session_state.backend = ChatbotBackend()

# Sidebar Navigation
mode = st.sidebar.radio("Navigation", ["Chatbot", "Admin Panel"])

if mode == "Admin Panel":
    render_admin_panel()
else:
    st.title("🍽️ AI Restaurant Assistant")
    st.markdown("ask me about our menu, hours, or policies!")

    # Initialize Chat History
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! Welcome to Spice AI. How can I help you today? 🍽️"}
        ]

    # Display Chat History
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # User Input
    if prompt := st.chat_input("How can I help you?"):
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate Response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = st.session_state.backend.process_message(
                    prompt, 
                    st.session_state.messages
                )
                st.markdown(response)
                
        # Add assistant response to history
        st.session_state.messages.append({"role": "assistant", "content": response})
