#!/usr/bin/env python3

import requests
import os

url = 'https://api.dropboxapi.com/oauth2/token'
app_key = os.environ.get('DROPBOX_KEY')
app_secret = os.environ.get('DROPBOX_SECRET')
access_code = os.environ.get("DROPBOX_AUTH_CODE")

headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

data = {
    'code': access_code,
    'grant_type': 'authorization_code'
}

auth = (app_key, app_secret)
response = requests.post(url, headers=headers, data=data, auth=auth)

print(response.text)