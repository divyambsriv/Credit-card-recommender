
import streamlit as st
from load_cards import CardDatabase

def display_comparison(cards):
    if not cards:
        st.warning("No cards to compare.")
        return

    st.markdown("## 🔍 Compare Recommended Credit Cards")

    for card in cards:
        with st.container():
            cols = st.columns([1, 2])
            with cols[0]:
                st.image(card["image_url"], width=100)
            with cols[1]:
                st.markdown(f"**{card['name']}**")
                st.markdown(f"- Issuer: {card['issuer']}")
                st.markdown(f"- Rewards: {card['reward_type']} ({card['reward_rate']})")
                st.markdown(f"- Perks: {card['perks']}")
                st.markdown(f"- Fees: ₹{card['joining_fee']} joining / ₹{card['annual_fee']} annual")
                st.markdown(f"[Apply Here]({card['link']})", unsafe_allow_html=True)
            st.markdown("---")
