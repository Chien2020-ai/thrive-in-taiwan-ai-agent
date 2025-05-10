# state_store.py

# Simple in-memory store for user language preference
user_language = {}

def set_user_language(user_id, lang):
    user_language[user_id] = lang

def get_user_language(user_id):
    return user_language.get(user_id, "en")
