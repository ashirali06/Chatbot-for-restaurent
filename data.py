import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

class DataManager:
    def __init__(self):
        self.menu_file = os.path.join(DATA_DIR, 'menu.json')
        self.faq_file = os.path.join(DATA_DIR, 'faq.json')
        self.config_file = os.path.join(DATA_DIR, 'config.json')

    def _load_json(self, filepath):
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            return {}

    def _save_json(self, filepath, data):
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)

    # Menu Methods
    def get_menu(self):
        return self._load_json(self.menu_file)

    def save_menu(self, menu_data):
        self._save_json(self.menu_file, menu_data)

    def get_menu_text(self):
        menu = self.get_menu()
        text = "🍽️ **Our Menu:**\n\n"
        for category, items in menu.items():
            text += f"**{category}**\n"
            for item in items:
                if item.get('available', True):
                    text += f"- {item['name']}: ${item['price']} ({item['description']})\n"
            text += "\n"
        return text.strip()

    # FAQ Methods
    def get_faq(self):
        return self._load_json(self.faq_file)

    def save_faq(self, faq_data):
        self._save_json(self.faq_file, faq_data)

    def search_faq(self, query):
        faqs = self.get_faq()
        query = query.lower()
        # Simple keyword matching
        for key, answer in faqs.items():
            if key in query:
                return answer
        return None

    # Config Methods
    def get_config(self):
        return self._load_json(self.config_file)

    def save_config(self, config_data):
        self._save_json(self.config_file, config_data)
