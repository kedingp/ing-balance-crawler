#!/usr/bin/env python3

import requests
import os

url = 'https://api.dropboxapi.com/oauth2/token'
app_key = os.environ.get('DROPBOX_KEY')
app_secret = os.environ.get('DROPBOX_SECRET')
refresh_token = os.environ.get("DROPBOX_REFRESH_TOKEN")

headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

data = {
    'refresh_token': refresh_token,
    'grant_type': 'refresh_token'
}

auth = (app_key, app_secret)
response = requests.post(url, headers=headers, data=data, auth=auth)

print(response.text)