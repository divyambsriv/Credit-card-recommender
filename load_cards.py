import json
import re

class CardDatabase:
    def __init__(self, json_path="cards.json"):
        with open(json_path, "r") as f:
            self.cards = json.load(f)

    def filter_by_income(self, monthly_income):
        return [
            card for card in self.cards
            if self._income_matches(card.get("eligibility", ""), monthly_income)
        ]

    def filter_by_reward_type(self, reward_type):
        return [
            card for card in self.cards
            if reward_type.lower() in card.get("reward_type", "").lower()
        ]

    def filter_by_perks(self, cards, user_perks):
        def matches_any(user_perk, card_perks):
            all_keywords = card.get("perks", []) + card.get("tags", [])
            return any(user_perk.lower() in p.lower() for p in all_keywords)

        return [
            card for card in cards
            if any(matches_any(perk, card) for perk in user_perks)
        ]

    def filter_by_spending(self, cards, user_spending):
        def matches_any(spend_term, card_perks):
            all_keywords = card.get("perks", []) + card.get("tags", [])
            return any(spend_term.lower() in p.lower() for p in all_keywords)

        return [
            card for card in cards
            if any(matches_any(spend, card) for spend in user_spending)
        ]

    def _income_matches(self, eligibility_text, income):
        # Matches patterns like: "Income ₹25,000/month", "₹1 Lakh", "₹70,000"
        if "proof" in eligibility_text.lower():
            return True
        match = re.search(r"[₹\s]*(\d{2,3})(k|000)?", eligibility_text.lower().replace(",", ""))
        if match:
            num = int(match.group(1))
            if match.group(2) in ["k", "000"]:
                num *= 1000
            return income >= num
        return True

    def get_top_cards(self, count=5):
        return self.cards[:count]
