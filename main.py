import time
import re
import requests
from bs4 import BeautifulSoup
from telegram import Bot
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Telegram bilgileri
TELEGRAM_TOKEN = "7001143599:AAHoOZYXycFQJ0rTl8z79DIK6DtP-E2oxio"
TELEGRAM_CHAT_ID = "7392451982"

bot = Bot(token=TELEGRAM_TOKEN)

def send_message(text):
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=text)
    except Exception as e:
        print("Mesaj gönderilemedi:", e)

def check_appointment():
    try:
        send_message("Patron Luis, çalışmaya başladım!")

        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, 20)

        driver.get("https://www.konsolosluk.gov.tr")

        # Ülke ve şehir seçimi
        wait.until(EC.element_to_be_clickable((By.ID, "ddlCountry"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//option[text()="Fas"]'))).click()
        wait.until(EC.element_to_be_clickable((By.ID, "ddlMission"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//option[contains(text(),"Rabat")]'))).click()
        wait.until(EC.element_to_be_clickable((By.ID, "btnSubmit"))).click()

        # Evlilik Tescili Başvurusu linkine tıkla
        wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Evlilik Tescili Başvurusu"))).click()

        # Randevu popup'ını yakala
        randevu_popup = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "swal2-popup")))
        randevu_text = randevu_popup.text

        # Tarihi çekmek için regex ile kontrol
        match = re.search(r"\d{2}\.\d{2}\.\d{4}", randevu_text)
        if match:
            tarih = match.group()
            mesaj = f"RANDEVU VAR!\nTarih: {tarih}\nYer: Rabat Büyükelçiliği"
            send_message(mesaj)
        else:
            send_message("Henüz yeni randevu bulunamadı.")

    except Exception as e:
        send_message(f"HATA OLUŞTU:\n{e}")
    
    finally:
        try:
            driver.quit()
        except:
            pass

# Çalıştır
if __name__ == "__main__":
    check_appointment()
