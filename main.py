import streamlit as st
from agent import process_user_message
from compare_ui import display_comparison

st.set_page_config(page_title="Credit Card Recommender", layout="centered")
st.title("💳 Smart Credit Card Recommender")

# Initialize chat state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "show_cards" not in st.session_state:
    st.session_state.show_cards = []

# Show welcome message if no conversation yet
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
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Process user input
    response = process_user_message(user_input, st.session_state.messages, st.session_state.answers)

    with st.chat_message("assistant"):
        st.markdown(response)

    # Store recommended cards
    if response.startswith("**Here are your top recommended credit cards:**"):
        from agent import run_card_recommendation
        cards, _ = run_card_recommendation(st.session_state.answers)
        st.session_state.show_cards = cards

    elif response.startswith("❌ No exact matches found."):
        from agent import run_card_recommendation
        cards, _ = run_card_recommendation(st.session_state.answers)
        st.session_state.show_cards = cards

# Show card comparison
if st.session_state.show_cards:
    display_comparison(st.session_state.show_cards)
