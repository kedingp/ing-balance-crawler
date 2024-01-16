import logging
import csv
import os
import requests
import time
import dotenv
import pickle
from time import sleep
import smtplib
from datetime import datetime


from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlencode, quote_plus
from pathlib import Path
from selenium import webdriver

logger = logging.getLogger("myLogger")
logger.setLevel(logging.INFO)
fh = logging.StreamHandler()
fh.setLevel(logging.INFO)
# create formatter and add it to the handlers
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)


csv_file_path = 'kontostaende.csv'

# Prüfen, ob die Datei bereits existiert
file_exists = os.path.isfile(csv_file_path)


opts = Options()
opts.headless = False
#opts.add_experimental_option('prefs', {'profile.default_content_setting_values.cookies': 1})
logging.info("Starte FireFox")

options = webdriver.ChromeOptions()

# Set preferences to enable cookies
options.add_experimental_option('prefs', {'profile.default_content_setting_values.cookies': 1})
options.add_experimental_option('prefs', {"profile.block_third_party_cookies": False})





#browser = Firefox(options=opts)

#Setzen der Variablen
url = os.environ.get('URL')
picturepath = os.environ.get('PICTUREPATH', '/tmp/home')
zugangsnummer_1 = os.environ.get('ZUGANGSNUMMER_1')
zugangsnummer_2 = os.environ.get('ZUGANGSNUMMER_2')
zugangsnummern = [zugangsnummer_1, zugangsnummer_2]
pin = os.environ.get('PIN')
gmail_pin = os.environ.get('GMAIL_PIN')
gmail_from = os.environ.get('GMAIL_FROM_ADDRESS')
gmail_to = os.environ.get('GMAIL_TO_ADRESS')

for zugangsnummer in zugangsnummern:
    logging.info("Oeffne Startseite")
    # Launch the browser with the modified preferences
    browser = webdriver.Chrome(options=options)
    browser.get(url)
    # Startseite#
    #/html/body/div[3]
    # Wait for the cookie popup to appear (adjust the timeout as needed)

    popup_element = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[contains(@id, "overlay-content--")]'))
    )

    zugang_field = browser.find_element(By.XPATH, '//*[@id="id6"]')

    while True:
        try:
            zugang_field.send_keys(zugangsnummer)
            break
        except Exception:
            sleep(2)
    pin_field = browser.find_element(By.XPATH, '//*[@id="id7"]')
    pin_field.send_keys(pin)

    # Keyeingabe
    try:
        browser.find_element(By.XPATH, '//*[@id="ida"]').click()
        # //*[@id="id19"]/label[1]/span[2]
        # //*[@id="id19"]/label[1]/span[2]
        browser.find_element(By.XPATH, '//*[@id="id19"]/label[1]/span[1]').click()
        browser.find_element(By.XPATH, '//*[@id="id17"]').click()
    except Exception:
        pass
# //*[@id="id897bb87e"]/span[1]
# /html/body/div[1]/div/main/div/div[1]/div/section[2]/div[1]/div/div/div[2]/a/span[5]/span[1]
    # creates SMTP session
    # s = smtplib.SMTP('smtp.gmail.com', 587, timeout=10)
    # # start TLS for security
    # s.starttls()
    # # Authentication
    # s.login(gmail_from, gmail_pin)
    # # message to be sent
    # message = "Subject: Kontostandsabfrage ING\nBitte bestaetige die Kontostandsabfrage in der Ing Banking App in den naechsten 20 Minuten."
    # # sending the mail
    # s.sendmail(gmail_from, gmail_to, message)
    # # terminating the session
    # s.quit()

    balance = WebDriverWait(browser, 1200).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/main/div/div[1]/div/section[2]/div[1]/div/div/div[2]/a/span[5]/span[1]'))).text
    browser.close()

    data = [
    {'date': datetime.now().strftime('%Y-%m-%d'), 'bank account': zugangsnummer, 'balance': balance.replace('.', '')},
    ]
    mode = 'a' if file_exists else 'w'
    last_id = 0
    with open(csv_file_path, mode, newline='') as csvfile:
        fieldnames = ['id', 'date', 'bank account', 'balance']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()
            file_exists = True
        else:
            # Wenn die Datei existiert, finde die letzte ID
            with open(csv_file_path, 'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                last_row = None
                for last_row in reader:
                    pass
                last_id = int(last_row['id']) if last_row else 0

        # Schreibe die Daten in die CSV-Datei
        for idx, row in enumerate(data, start=last_id + 1):
            row['id'] = idx
            writer.writerow(row)
