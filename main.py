import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import telegram

TELEGRAM_TOKEN = '7001143599:AAHoOZYnycFQJ0rTl8z79DIK6DtP-E2oxio'
TELEGRAM_CHAT_ID = '7392451982'

bot = telegram.Bot(token=TELEGRAM_TOKEN)

try:
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="Patron Luis, çalışmaya başladım!")

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 20)

    driver.get("https://www.konsolosluk.gov.tr")

    time.sleep(2)
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btn-primary"))).click()

    wait.until(EC.element_to_be_clickable((By.ID, "ddlCountry"))).click()
    driver.find_element(By.XPATH, "//option[contains(text(), 'Fas')]").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//option[contains(text(), 'Rabat')]").click()
    time.sleep(1)
    driver.find_element(By.ID, "btnSubmit").click()
    time.sleep(3)

    wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Evlilik Tescili Başvurusu"))).click()
    time.sleep(4)

    randevu_popup = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "swal2-popup")))
    randevu_text = randevu_popup.text

    if "Randevular" in randevu_text and "Rabat" in randevu_text:
        lines = randevu_text.split("\n")
        tarih = "TARİH BULUNAMADI"
        for line in lines:
            if any(char.isdigit() for char in line) and "." in line:
                tarih = line.strip()
                break

        mesaj = f"**RANDEVU VAR!**\nTarih: {tarih}\nYer: Rabat Büyükelçiliği"
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=mesaj)
    else:
        print("Şu anda randevu görünmüyor.")

except Exception as e:
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=f"*HATA OLUŞTU:*\n{e}")
finally:
    driver.quit()