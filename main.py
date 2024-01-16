import logging
import smtplib
import csv
import os
from time import sleep
from datetime import datetime


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

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


#opts.add_experimental_option('prefs', {'profile.default_content_setting_values.cookies': 1})
logging.info("Starte Chrome")


chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")




#browser = Firefox(options=opts)

#Setzen der Variablen
url = os.environ.get('ING_URL')
zugangsnummer_1 = os.environ.get('ING_ZUGANGSNUMMER_1')
zugangsnummer_2 = os.environ.get('ING_ZUGANGSNUMMER_2')
zugangsnummern = [zugangsnummer_1, zugangsnummer_2]
pin = os.environ.get('ING_PIN')
gmail_pin = os.environ.get('GMAIL_PIN')
gmail_from = os.environ.get('GMAIL_FROM_ADDRESS')
gmail_to = os.environ.get('GMAIL_TO_ADRESS')

for zugangsnummer in zugangsnummern:
    logging.info("Oeffne Startseite")
    # Launch the browser with the modified preferences
    browser = webdriver.Chrome(options=chrome_options)
    browser.get(url)
    # Startseite#
    #/html/body/div[3]
    # Wait for the cookie popup to appear (adjust the timeout as needed)

    popup_element = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[contains(@id, "overlay-content--")]'))
    )
# //*[@id="dialogContent-na3zqnfcsp"]//ing-cc-button-87217[1]
    #//*[@id="dialogContent-gnkpwj47d6"]
# /html/body/div[3]/div[2]/ing-cc-dialog-frame-87215/ing-cc-dialog-level0-87212//ing-cc-button-87217[1]
    #//*[@id="dialogContent-6nx5r5surc"]
    # Now, find the specific button within the popup using a relative XPath
    # //*[@id="dialogContent-cqnsdh0e0b"]
    # //*[@id="dialogContent-cqnsdh0e0b"]//div[3]
    #//*[@id="dialogContent-1cwzaejzzw"]//div[3]/a[1]//*[@id="dialogContent-znjvxpr4uk"]//ing-cc-button-40828[1]
    #//*[@id="dialogContent-h260cn1xz3"]
    input = """return document.querySelector('[id^="dialogContent-"]').shadowRoot.querySelector('[data-tag-name="ing-cc-button"]')"""

    WebDriverWait(browser, 20).until(EC.element_to_be_clickable((browser.execute_script(input)))).click()

    # def expand_shadow_element(element):
    #     shadow_root = browser.execute_script('return arguments[0].shadowRoot', element)
    #     return shadow_root

    # outer = expand_shadow_element(popup_element)
    # inner = outer.find_element(By.XPATH, '//*[contains(@id, "ing-cc-button")]')
    # inner.click()
        


    zugang_field = browser.find_element(By.XPATH, '//*[@id="id6"]')
    counter = 0
    while True:
        try:
            zugang_field.send_keys(zugangsnummer)
            break
        except Exception:
            if counter >= 5:
                raise Exception("Cookies haven't been accepted. Stop continuation.")
            counter += 1
            sleep(2)
    pin_field = browser.find_element(By.XPATH, '//*[@id="id7"]')
    pin_field.send_keys(pin)

    # Keyeingabe
    try:
        browser.find_element(By.XPATH, '//*[@id="ida"]').click()
        browser.find_element(By.XPATH, '//*[@id="id19"]/label[1]/span[1]').click()
        browser.find_element(By.XPATH, '//*[@id="id17"]').click()
    except Exception:
        pass
    s = smtplib.SMTP('smtp.gmail.com', 587, timeout=10)
    # start TLS for security
    s.starttls()
    # Authentication
    s.login(gmail_from, gmail_pin)
    # message to be sent
    message = f"Subject: Kontostandsabfrage ING\nBitte bestaetige die Kontostandsabfrage fuer das Konto {zugangsnummer} in der Ing Banking App in den naechsten 20 Minuten."
    # sending the mail
    s.sendmail(gmail_from, gmail_to, message)
    # terminating the session
    s.quit()

    balance = WebDriverWait(browser, 1200).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/main/div/div[1]/div/section[2]/div[1]/div/div/div[2]/a/span[5]/span[1]'))).text
    browser.close()

    print(f"balance: {balance}")
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
