### Credit-card-recommender

## 💳 Smart Credit Card Recommender

This is a Streamlit-based web application that uses an AI-powered conversational agent to recommend the best credit cards for users in India based on income, spending habits, and desired perks.

---

## 🚀 Features

- 🤖 LLM-powered conversation
- 📊 Dynamic credit card filtering based on user inputs
- 📚 Pre-loaded database of credit cards (`cards.json`)
- 🧾 Visual comparison of recommended cards
- 🧠 Designed for quick personalization & high match quality

---
## 🛠️ Setup Instructions

1. Clone the repo and install requirements:
```bash
pip install -r requirements.txt
```

2. Add your OpenAI key:
Create a file: `.streamlit/secrets.toml`
```toml
OPENAI_API_KEY = "your-key-here"
GEMINI_API_KEY = "your-key-here"
```

3. Run the app:
```bash
streamlit run main.py
```

---

## 📂 Files

- `main.py` — Streamlit frontend & chat UI
- `agent.py` — Agent logic & recommendation engine
- `compare_ui.py` — Visual card comparison renderer
- `cards.json` — Sample credit card data (20+ entries)
- `load_cards.py` — Loads and filters card data
