import streamlit as st
import google.generativeai as genai
from compare_ui import display_comparison

# 🔑 Configure Gemini (set your API key in Streamlit secrets or env)
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Initialize Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

st.set_page_config(page_title="Credit Card Recommender", layout="centered")
st.title("💳 Smart Credit Card Recommender")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "show_cards" not in st.session_state:
    st.session_state.show_cards = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Show welcome message
if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.markdown("""
👋 Welcome! I can help you find the best credit card based on your lifestyle and preferences.

What is your monthly income in ₹?
""")

# Display previous chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input box
if user_input := st.chat_input("Ask anything about credit cards..."):
    # Store user input
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Send message to Gemini
    response = st.session_state.chat_session.send_message(user_input)

    # Extract text
    ai_reply = response.candidates[0].content.parts[0].text.strip()

    # Store and show response
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
    with st.chat_message("assistant"):
        st.markdown(ai_reply)

    # Example: detect if Gemini gave recommendations (adjust logic)
    if ai_reply.startswith("**Here are your top recommended credit cards:**"):
        # You’ll need to replace this with Gemini’s structured response or your own logic
        from agent import run_card_recommendation
        cards, _ = run_card_recommendation(st.session_state.answers)
        st.session_state.show_cards = cards

    elif ai_reply.startswith("❌ No exact matches found."):
        from agent import run_card_recommendation
        cards, _ = run_card_recommendation(st.session_state.answers)
        st.session_state.show_cards = cards

# Show card comparison if cards exist
if st.session_state.show_cards:
    display_comparison(st.session_state.show_cards)
