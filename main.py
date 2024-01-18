import smtplib
import csv
import os
from datetime import datetime
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import dropbox_utility

login_attempts = 0

def write_mail(from_address, to_address, message):
    # send email
    s = smtplib.SMTP("smtp.gmail.com", 587, timeout=10)
    s.starttls()
    s.login(from_address, gmail_pin)
    s.sendmail(from_address, to_address, message)
    s.quit()

try:
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")

    # Variables
    url = os.environ.get("ING_URL")
    zugangsnummer_1 = os.environ.get("ING_ZUGANGSNUMMER_1")
    zugangsnummer_2 = os.environ.get("ING_ZUGANGSNUMMER_2")
    zugangsnummern = [zugangsnummer_1, zugangsnummer_2]
    ing_pin = os.environ.get("ING_PIN")
    gmail_pin = os.environ.get("GMAIL_PIN")
    gmail_from = os.environ.get("GMAIL_FROM_ADDRESS")
    gmail_to = os.environ.get("GMAIL_TO_ADRESS")
    dropbox_access_token = dropbox_utility.get_access_token()
    csv_file_path = "kontostaende.csv"
    dropbox_file_path = "/" + csv_file_path

    # Prüfen, ob die Datei bereits existiert
    file_exists = csv_file_path in dropbox_utility.all_files_in_folder(
        dropbox_access_token
    )
    if file_exists:
        dropbox_utility.download_file(
            dropbox_access_token, dropbox_file_path, csv_file_path
        )

    def get_balance():
        global login_attempts
        browser = webdriver.Chrome(options=chrome_options)
        browser.get(url)

        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[contains(@id, "overlay-content--")]')
            )
        )

        # to make sure that the accept button is available
        sleep(2)

        # this is necessary to get access to shadowRoot elements. In this case the accept button of the cookies.
        java_script_input = """return document.querySelector('[id^="dialogContent-"]').shadowRoot.querySelector('[data-tag-name="ing-cc-button"]')"""
        WebDriverWait(browser, 20).until(
            EC.element_to_be_clickable((browser.execute_script(java_script_input)))
        ).click()

        zugang_field = browser.find_element(By.XPATH, '//*[@id="id6"]')
        zugang_field.send_keys(zugangsnummer)
        pin_field = browser.find_element(By.XPATH, '//*[@id="id7"]')
        pin_field.send_keys(ing_pin)

        # Necessary for accounts with more than one banking app atached
        try:
            browser.find_element(By.XPATH, '//*[@id="ida"]').click()
            browser.find_element(By.XPATH, '//*[@id="id19"]/label[1]/span[1]').click()
            browser.find_element(By.XPATH, '//*[@id="id17"]').click()
        except Exception:
            pass
        
        try:
            result = (
                WebDriverWait(browser, 300)
                .until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            "/html/body/div[1]/div/main/div/div[1]/div/section[2]/div[1]/div/div/div[2]/a/span[5]/span[1]",
                        )
                    )
                )
                .text
            )
        except Exception:
            browser.close()
            if login_attempts > 4:
                return None
            login_attempts += 1
            get_balance()
        browser.close()
        return result


    for zugangsnummer in zugangsnummern:
        message = f"Subject: Kontostandsabfrage ING\nBitte bestaetige die Kontostandsabfrage fuer das Konto {zugangsnummer} in der Ing Banking App in den naechsten 20 Minuten."
        write_mail(gmail_from, gmail_to, message)

        # Launch the browser with the modified preferences
        print("Waiting for two-factor authentication...")
        balance = get_balance()
        if not balance:
            raise ValueError("Two-factor authentication timed out!")
        print("Received two-factor authentication!")

        data = [
            {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "bank account": zugangsnummer,
                "balance": balance.replace(".", ""),
            },
        ]
        mode = "a" if file_exists else "w"
        last_id = 0
        with open(csv_file_path, mode, newline="") as csvfile:
            fieldnames = ["id", "date", "bank account", "balance"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            if not file_exists:
                writer.writeheader()
                file_exists = True
            else:
                # if file exists find last id
                with open(csv_file_path, "r", newline="") as csvfile:
                    reader = csv.DictReader(csvfile)
                    last_row = None
                    for last_row in reader:
                        pass
                    last_id = int(last_row["id"]) if last_row else 0

            for idx, row in enumerate(data, start=last_id + 1):
                row["id"] = idx
                writer.writerow(row)

    dropbox_utility.upload_file(dropbox_access_token, csv_file_path, dropbox_file_path)

except Exception as e:
    message = f"Subject: Fehler in Kontostandsabfrage ING\nEs gab einen Fehler bei der Kontostandsabfrage: {e}. Bitte kontrolliere die Pipeline."
    write_mail(gmail_from, gmail_to, message)
