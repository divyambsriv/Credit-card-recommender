import openai
import os
import json
import re
from load_cards import CardDatabase

openai.api_key = os.getenv("OPENAI_API_KEY")
REQUIRED_FIELDS = ["income", "spending", "perks"]

def ask_gpt_for_answers(user_input):
    system_prompt = """
You are a helpful assistant for a credit card recommendation app.

Given a user message, extract these:
{
  "income": inferred monthly income as an integer, or null,
  "spending": list of major spending areas, e.g. ["fuel", "groceries"], or [],
  "perks": list of desired perks like ["cashback", "lounge access"], or [],
}

Respond ONLY with JSON.
"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]
        )
        content = response.choices[0].message["content"]
        print("\U0001f9e0 GPT Parsed:", content)
        return json.loads(content)
    except Exception as e:
        print("❌ Error parsing GPT response:", e)
        return {}

def keyword_fallback(user_message):
    lowered = user_message.lower()
    result = {}

    income_match = re.search(r"(\u20b9|\brs)?\s?(\d{2,3})(k|\s?lakh|k\b|000)?", lowered)
    if income_match:
        num = int(income_match.group(2))
        if income_match.group(3):
            if "lakh" in income_match.group(3):
                num *= 100000
            else:
                num *= 1000
        result["income"] = num

    spending_keywords = {
    "fuel": "fuel",
    "travel": "travel",
    "grocery": "groceries",
    "groceries": "groceries",
    "shopping": "shopping",
    "dining": "dining",
    "subscriptions": "subscriptions"
}
    result["spending"] = [v for k, v in spending_keywords.items() if k in lowered]

    perk_keywords = {
    "cashback": "cashback",
    "lounge access": "lounge access",
    "lounge": "lounge access",
    "airport lounge": "lounge access",
    "travel points": "travel points",
    "voucher": "amazon vouchers",
    "amazon": "amazon vouchers",
    "dining offer": "dining offers",
    "dining offers": "dining offers"
}
    result["perks"] = list(set([v for k, v in perk_keywords.items() if k in lowered]))

    if not result.get("spending"):
        result.pop("spending", None)
    if not result.get("perks"):
        result.pop("perks", None)

    return result

def get_next_question(answers):
    for field in REQUIRED_FIELDS:
        if field not in answers or not answers[field]:
            if field == "income":
                return "What is your monthly income in rupees?"
            if field == "spending":
                return "How do you spend the most money on? (e.g., fuel, groceries, travel)"
            if field == "perks":
                return "What kind of credit card perks do you care about the most? (e.g., cashback, lounge access)"
    return None

def is_ready(answers):
    return all(field in answers and answers[field] for field in REQUIRED_FIELDS)

def run_card_recommendation(answers):
    db = CardDatabase("cards.json")
    cards = db.filter_by_income(answers.get("income", 0))

    if "spending" in answers:
        try:
            cards = db.filter_by_spending(cards, answers["spending"])
        except:
            pass

    if "perks" in answers:
        try:
            cards = db.filter_by_perks(cards, answers["perks"])
        except:
            pass

    return cards[:3], db

def process_user_message(user_message, chat_history, answers):
    if user_message.lower().strip() in ["restart", "reset", "start over"]:
        answers.clear()
        chat_history.clear()
        return "✅ Conversation restarted.\n\nWhat is your monthly income in rupees?"

    chat_history.append({"role": "user", "content": user_message})
    extracted = ask_gpt_for_answers(user_message) or keyword_fallback(user_message)

    for key in ["income", "spending", "perks"]:
        if extracted.get(key):
            answers[key] = extracted[key]

    print("📦 Final collected answers:", answers)

    if is_ready(answers):
        cards, db = run_card_recommendation(answers)
        if cards:
            card_lines = [
                f"""🔹 {card['name']} ({card['issuer']})
💰 Rewards: {card['reward_type']} – {card['reward_rate']}
🎁 Perks: {', '.join(card.get('perks', []))}
🧾 Fees: ₹{card['joining_fee']} joining / ₹{card['annual_fee']} annual
🔗 [Apply Now]({card['link']})
""" for card in cards
            ]
            return "Here are your top recommended credit cards:\n\n" + "\n".join(card_lines) + "\n\nYou can type 'restart' to try again. 🔄"

        else:
            fallback = db.filter_by_income(answers["income"])[:3]
            fallback_lines = [
                f"🔸 {card['name']} ({card['issuer']}) – {card['reward_type']}: {card['reward_rate']}"
                for card in fallback
            ]
            return (
                "❌ No exact matches found.\n\n"
                "Here are some other good cards based on your income:\n\n" +
                "\n".join(fallback_lines) +
                "\n\nYou can type 'restart' to try again."
            )

    return get_next_question(answers)
