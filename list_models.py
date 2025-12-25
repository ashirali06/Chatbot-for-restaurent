import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Fallback Key logic (same as llm_helper.py)
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    API_KEY = "AIzaSyDoZRuJRRveu-gO1EgDQGqR3SO9UQdA7OQ"

genai.configure(api_key=API_KEY)

try:
    print("Listing models...")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)
except Exception as e:
    print(f"Error: {e}")
