from data import DataManager
from llm_helper import get_ai_response

class ChatbotBackend:
    def __init__(self):
        self.data_manager = DataManager()
        self.menu_keywords = ["menu", "price", "cost", "starter", "main course", "drink", "items", "list"]
        self.faq_keywords = ["open", "close", "hour", "time", "location", "address", "where", "halal", "veg", "delivery", "book", "reservation"]
        
        # Strict System Prompt
        self.system_prompt = """
        You are an AI Restaurant Assistant.
        Your goal is to be polite, professional, and helpful.
        If the user asks a question that is NOT about the menu or standard FAQs, respond politely.
        Keep responses under 80 words.
        Use simple English or Roman Urdu.
        Use emojis sparingly 🍽️🙂.
        NEVER hallucinate menu items or policies.
        NEVER mention Gemini, internal systems, or databases.
        """

    def process_message(self, user_message, chat_history=[]):
        user_message_lower = user_message.lower()

        # 1. MENU QUERIES
        # Check if the user is explicitly asking for the menu or prices
        if any(keyword in user_message_lower for keyword in self.menu_keywords):
            # A simple keyword match might be too aggressive (e.g. "I don't like food"), 
            # but for an MVP strict rule, it ensures we show the menu.
            # To be smarter, we could use the LLM to classify, but the user requested strict routing.
            # Let's check if it's a question or a request roughly.
            return self.data_manager.get_menu_text()

        # 2. FAQ QUERIES
        if any(keyword in user_message_lower for keyword in self.faq_keywords):
            answer = self.data_manager.search_faq(user_message_lower)
            if answer:
                return answer
            # If keyword matches but no exact FAQ found, fall through to LLM 
            # OR return a generic help message? 
            # The prompt says: "Call search_faq... If an answer exists, return it exactly."
            # If not found, it falls to General Conversation.

        # 3. GENERAL CONVERSATION / FALLBACK
        # Transform chat_history to Gemini format if needed (list of dicts)
        gemini_history = []
        for msg in chat_history:
            role = "user" if msg["role"] == "user" else "model"
            gemini_history.append({"role": role, "parts": [msg["content"]]})

        return get_ai_response(gemini_history, user_message, self.system_prompt)
