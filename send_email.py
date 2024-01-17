import smtplib
import dotenv
import os

gmail_pin = os.environ.get('GMAIL_PIN')
gmail_from = os.environ.get('GMAIL_FROM_ADDRESS')
gmail_to = os.environ.get('GMAIL_TO_ADRESS')

s = smtplib.SMTP('smtp.gmail.com', 587, timeout=10)
# start TLS for security
s.starttls()
# Authentication
s.login(gmail_from, gmail_pin)
# message to be sent
message = "Subject: Kontostandsabfrage ING\nBitte bestaetige die Kontostandsabfrage in der Ing Banking App in den naechsten 20 Minuten."
# sending the mail
s.sendmail(gmail_from, gmail_to, message)
# terminating the session
s.quit()