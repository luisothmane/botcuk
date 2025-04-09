import requests
from bs4 import BeautifulSoup
import telegram
import time

TELEGRAM_TOKEN = "7001143599:AAHoOZYXycFQJ0rTl8z79DIK6DtP-E2oxio"
TELEGRAM_CHAT_ID = "7392451982"

bot = telegram.Bot(token=TELEGRAM_TOKEN)

def send_message(text):
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=text)
    except Exception as e:
        print("Mesaj gönderilemedi:", e)

def check_appointment():
    try:
        session = requests.Session()

        # Ülke ve temsilcilik seçimi için ilk sayfa
        base_url = "https://www.konsolosluk.gov.tr"
        randevu_url = f"{base_url}/"
        response = session.get(randevu_url)
        soup = BeautifulSoup(response.text, "html.parser")

        # Gerekli POST istekleriyle ülke ve temsilcilik seçimleri yapılacak
        # Bu bölümde Selenium kullanmak gerekir çünkü JavaScript ile açılan popup'lar var.
        # GitHub Actions gibi headless ortamlarda bu işlemi sadece HTML ile yapmak mümkün değildir.

        # Şimdilik mesaj gönderimi simülasyonu:
        send_message("Patron Luis, çalışmaya başladım!")

        # Randevu sayfasını ziyaret et (örnek)
        dummy_check_url = f"{base_url}/appointments"
        response = session.get(dummy_check_url)

        if "Randevu" in response.text:
            send_message("Yeni randevu kontrolü yapıldı!")
        else:
            send_message("Henüz yeni randevu bulunamadı.")

    except Exception as e:
        send_message(f"HATA OLUŞTU:\n{e}")

if __name__ == "__main__":
    check_appointment()
