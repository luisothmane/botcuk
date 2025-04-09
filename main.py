import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from telegram import Bot

# Telegram bilgileri (kendine göre düzenle)
TELEGRAM_TOKEN = "7001143599:AAHoOZYXycFQJ0rTl8z79DIK6DtP-E2oxio"
TELEGRAM_CHAT_ID = "7392451982"  # Senin Telegram ID'in

# Telegram mesaj fonksiyonu
def send_message(text):
    try:
        bot = Bot(token=TELEGRAM_TOKEN)
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=text)
    except Exception as e:
        print("Telegram mesaj hatası:", e)

# Ana randevu kontrol fonksiyonu
def check_appointment():
    try:
        send_message("Patron Luis, çalışmaya başladım!")

        # Headless Chrome başlat
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=options)

        # Doğrudan işlem sayfasına git
        driver.get("https://www.konsolosluk.gov.tr/Appointment/Index/5018")
        time.sleep(4)

        # Sayfa kaynağını al ve kontrol et
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        # Randevu tarihi arayan kısım
        tarih_td = soup.find("td", string=lambda text: text and "2025" in text)
        if tarih_td:
            mesaj = f"*RANDEVU VAR!*\nTarih: {tarih_td.text.strip()}\nYer: Rabat Büyükelçiliği"
            send_message(mesaj)
        else:
            send_message("Henüz yeni randevu bulunamadı.")

        driver.quit()

    except Exception as e:
        send_message(f"HATA OLUŞTU:\n{e}")

# Çalıştır
if __name__ == "__main__":
    check_appointment()
