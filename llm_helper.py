import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Try getting from Streamlit secrets first (for Cloud)
try:
    import streamlit as st
    if "GEMINI_API_KEY" in st.secrets:
        API_KEY = st.secrets["GEMINI_API_KEY"]
    else:
        API_KEY = os.getenv("GEMINI_API_KEY")
except ImportError:
    API_KEY = os.getenv("GEMINI_API_KEY")

if API_KEY:
    try:
        genai.configure(api_key=API_KEY)
    except Exception as e:
        print(f"Error configuring Gemini: {e}")

def get_ai_response(history, user_input, system_instruction):
    """
    Generates a response from Gemini using the provided history and system instruction.
    """
    if not API_KEY:
        return "System Error: API Key is missing. Please contact the administrator."

    try:
        model = genai.GenerativeModel(
            model_name="gemini-flash-latest",
            system_instruction=system_instruction
        )
        
        chat = model.start_chat(history=history)
        response = chat.send_message(user_input)
        return response.text.replace("\n", " ") # Keep it concise as requested

    except Exception as e:
        print(f"DEBUG ERROR: {e}") # Keep for debugging
        if "429" in str(e) or "ResourceExhausted" in str(e):
            return "I am currently receiving too many requests. Please wait 10 seconds and try again. 🕒"
        return "I apologize, but I am having trouble connecting to my brain right now. Please try again later."
