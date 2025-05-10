import json
import os

def load_faq(lang):
    file_path = os.path.join("faq_data", f"family_faq_{lang}.json")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def get_answer(user_input, lang):
    faqs = load_faq(lang)
    user_input_lower = user_input.lower()
    for item in faqs:
        if user_input_lower in item["question"].lower():
            return item["answer"]
    return {
        "en": "❓ Sorry, I couldn’t find a matching answer. You can try rephrasing or ask something else.",
        "zh": "❓ 抱歉，找不到對應的答案，請嘗試重新敘述或詢問其他問題喔。"
    }.get(lang, "No answer found.")
