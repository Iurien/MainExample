import requests
from django.conf import settings

def send_telegram_message(text):
    token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID
    if token and chat_id:
        url = f"https://api.telegram.org{token}/sendMessage"
        data = {"chat_id": chat_id, "text": text}
        try:
            requests.post(url, data=data)
        except Exception as e:
            print(f"Ошибка отправки в Telegram: {e}")