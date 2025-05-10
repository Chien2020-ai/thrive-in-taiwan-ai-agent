# main.py
from fastapi import FastAPI, Request
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os
from dotenv import load_dotenv
from faq_router import get_answer
from state_store import set_user_language, get_user_language

load_dotenv()

app = FastAPI()
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

@app.post("/callback")
async def callback(request: Request):
    body = await request.body()
    signature = request.headers.get("X-Line-Signature")
    handler.handle(body.decode("utf-8"), signature)
    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    text = event.message.text.strip().lower()

    if text in ["a", "english", "/lang en"]:
        set_user_language(user_id, "en")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="✅ Language set to English. How can I help you?")
        )
        return

    if text in ["b", "chinese", "/lang zh"]:
        set_user_language(user_id, "zh")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="✅ 語言已設定為中文。請問需要什麼協助？")
        )
        return

    user_lang = get_user_language(user_id) or "en"
    answer = get_answer(text, user_lang)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=answer)
    )
