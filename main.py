import requests
from bs4 import BeautifulSoup
from telegram import Bot
import os

# Telegram token ve chat ID ortam değişkenlerinden alınır
TELEGRAM_TOKEN = os.getenv("7001143599:AAHoOZYXycFQJ0rTl8z79DIK6DtP-E2oxio")
TELEGRAM_CHAT_ID = os.getenv("7392451982")

bot = Bot(token=TELEGRAM_TOKEN)

def send_message(message):
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

def check_appointment():
    try:
        send_message("Patron Luis, çalışmaya başladım!")

        url = "https://konsolosluk.gov.tr/Appointment/Index/5018"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")

        # 2025 içeren <td> etiketini bul
        date_td = soup.find("td", string=lambda text: text and "2025" in text)

        if date_td:
            send_message(f"YENİ RANDEVU VAR: {date_td.text.strip()}")
        else:
            send_message("Henüz yeni randevu bulunamadı.")
    except Exception as e:
        send_message(f"HATA OLUŞTU:\n{e}")

if __name__ == "__main__":
    check_appointment()
