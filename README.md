### Credit-card-recommender

## 💳 Smart Credit Card Recommender

This is a Streamlit-based web application that uses an AI-powered conversational agent to recommend the best credit cards for users in India based on income, spending habits, and desired perks.

---

## 🚀 Features

- 🤖 LLM-powered conversation flow using OpenAI API
- 📊 Dynamic credit card filtering based on user inputs
- 📚 Pre-loaded database of credit cards (`cards.json`)
- 🧾 Visual comparison of recommended cards
- 🧠 Designed for quick personalization & high match quality

---

## 🎥 Demo Video

https://github.com/divyamsbriv/Credit-card-recommender/assets/your-github-id/App-record.mp4


## Access app from here

https://my-credit-card-recommender.streamlit.app/

## 🛠️ Setup Instructions

1. Clone the repo and install requirements:
```bash
pip install -r requirements.txt
```

2. Add your OpenAI key:
Create a file: `.streamlit/secrets.toml`
```toml
OPENAI_API_KEY = "your-key-here"
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

## To run in colab

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/divyamsbriv/Credit-card-recommender/blob/main/credit_card_recommender.ipynb)
