# AI Restaurant Assistant 🍽️

A Streamlit-based AI chatbot for restaurant assistance, capable of handling menu queries, FAQs, and general conversation using Google Gemini.

## Features
- **Menu Queries**: Fetches menu items and prices from a local database.
- **FAQ Handling**: Answers common questions about hours, location, etc.
- **AI Conversation**: Uses Google Gemini for polite and helpful responses.
- **Admin Panel**: Manage menu items and FAQs.

## Setup

1.  **Clone the repository** (if not already local).
2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Set up Environment Variables**:
    - Create a `.env` file in the root directory.
    - Add your Gemini API key:
        ```
        GEMINI_API_KEY=your_api_key_here
        ```

## Running Locally

```bash
streamlit run app.py
```

## Deployment to Streamlit Cloud

1.  Push this code to a GitHub repository.
2.  Log in to [Streamlit Cloud](https://streamlit.io/cloud).
3.  Connect your GitHub account and select this repository.
4.  In the "Advanced Settings" of the deployment page, add your API key to **Secrets**:
    ```toml
    GEMINI_API_KEY = "your_api_key_here"
    ```
5.  Click **Deploy**!
