import os
import requests
import time

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import WebDriverException
from urllib.parse import urlencode, quote_plus
from pathlib import Path
from pprint import pprint

opts = Options()
opts.headless = True
print("Starte FireFox")
browser = Firefox(options=opts)

#Setzen der Variablen
url = os.environ.get('URL')
picturepath = os.environ.get('PICTUREPATH', '/tmp/home')
zugangsnummer = os.environ.get('ZUGANGSNUMMER')
pin = os.environ.get('PIN')
key = os.environ.get('KEY')
telegrambotkey = os.environ.get('TELEGRAMBOTKEY')
chatid = os.environ.get('CHATID')

print("Oeffne Startseite")

# Startseite
browser.get(url)
time.sleep(15)
browser.get_screenshot_as_file(picturepath + "/1.png")
browser.find_element_by_xpath("/html/body/div[1]/div/main/div[2]/div/fieldset/div/form/div[1]/span/input").send_keys(zugangsnummer)
browser.find_element_by_xpath("/html/body/div[1]/div/main/div[2]/div/fieldset/div/form/div[2]/span/input").send_keys(pin)

# Keyeingabe
browser.find_element_by_xpath('/html/body/div[1]/div/main/div[2]/div/fieldset/div/form/div[3]/div/div/div[1]/button').submit()
time.sleep(15)
browser.get_screenshot_as_file(picturepath + "/2.png")

# Es werden alle 6 Felder geprüft und bei Bedarf befüllt.
keybuttons = ["/html/body/div[1]/div/main/div/div/form/div/div[1]/div[2]/div/div[3]/div[4]/a[1]",
              "/html/body/div[1]/div/main/div/div/form/div/div[1]/div[2]/div/div[3]/div[1]/a[1]",
              "/html/body/div[1]/div/main/div/div/form/div/div[1]/div[2]/div/div[3]/div[1]/a[2]",
              "/html/body/div[1]/div/main/div/div/form/div/div[1]/div[2]/div/div[3]/div[1]/a[3]",
              "/html/body/div[1]/div/main/div/div/form/div/div[1]/div[2]/div/div[3]/div[2]/a[1]",
              "/html/body/div[1]/div/main/div/div/form/div/div[1]/div[2]/div/div[3]/div[2]/a[2]",
              "/html/body/div[1]/div/main/div/div/form/div/div[1]/div[2]/div/div[3]/div[2]/a[3]",
              "/html/body/div[1]/div/main/div/div/form/div/div[1]/div[2]/div/div[3]/div[3]/a[1]",
              "/html/body/div[1]/div/main/div/div/form/div/div[1]/div[2]/div/div[3]/div[3]/a[2]",
              "/html/body/div[1]/div/main/div/div/form/div/div[1]/div[2]/div/div[3]/div[3]/a[3]"]

for i in range(len(key)):
    keyfield = browser.find_element_by_xpath("/html/body/div[1]/div/main/div/div/form/div/div[1]/div[2]/div/div[2]/ul/li[" + str(i+1) + "]")
    if keyfield.get_attribute("class") == "active focus":
        print(key[i])
        browser.find_element_by_xpath(keybuttons[int(key[i])]).click()
        time.sleep(5)
        break


browser.get_screenshot_as_file(picturepath + "/3.png")

for j in range(len(key)):
    keyfield = browser.find_element_by_xpath("/html/body/div[1]/div/main/div/div/form/div/div[1]/div[2]/div/div[2]/ul/li[" + str(j+1) + "]")
    if keyfield.get_attribute("class") == "active focus":
        print(key[j])
        browser.find_element_by_xpath(keybuttons[int(key[j])]).click()
        time.sleep(5)
        break


browser.get_screenshot_as_file(picturepath + "/4.png")

browser.find_element_by_xpath("/html/body/div[1]/div/main/div/div/form/div/section/div/button[1]").click()
time.sleep(15)

browser.get_screenshot_as_file(picturepath + "/5.png")
balance = browser.find_element_by_xpath('/html/body/div[1]/div/main/div/div/div/section[2]/div[1]/div[1]/div[1]/div[2]/a/span[4]/span[1]').text

print(balance)

# Logout
browser.find_element_by_xpath('/html/body/div[1]/div/navigation-header/div/div/div[3]/ing-diba-session/ing-diba-session-button/a').click()
time.sleep(20)
try:
    browser.get_screenshot_as_file(picturepath + "/6.png")
except WebDriverException:
    print("Screenshot 6 kann nicht gespeichert werden...")

browser.quit()

# Alten Wert aus Datei lesen und vergleichen
my_file = Path(picturepath + "/balance.txt")
if not my_file.exists():
    filestore = open(picturepath + "/balance.txt", "w")
    filestore.write("0")
    filestore.close()

filestore = open(picturepath + "/balance.txt", "r")
oldbalance = filestore.read()
filestore.close()

text = ""
if balance != oldbalance:
    text = "ING-Diba: Neue Kontobewegung - Änderung von " + oldbalance + "€ auf " + balance + "€"
    payload = {'chat_id': chatid, 'text': text}
    result = urlencode(payload, quote_via=quote_plus)
    r = requests.get("https://api.telegram.org/" + telegrambotkey + "/sendMessage?" + result)
    pprint(r.json())
    filestore = open(picturepath + "/balance.txt", "w")
    filestore.write(balance)
    filestore.close()


exit(0)