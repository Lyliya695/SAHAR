import requests
from django.conf import settings

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": settings.TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, data=data, timeout=5)
        print(f"📥 Статус ответа: {response.status_code}")
        print(f"📥 Текст ответа: {response.text}")
                
        if response.status_code == 200:
                print("✅ Уведомление успешно отправлено!")
        else:
                print(f"❌ Ошибка отправки: {response.text}")
    except Exception as e:
        print("Telegram error:", e)




def send_telegram_to_user(user, text):
    if not user.profile.telegram_chat_id:
        return
# https://api.telegram.org/botсюда вставить токен/getUpdates
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": user.profile.telegram_chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    requests.post(url, data=data)
