#!/usr/bin/env python3

import requests
import os
def get_access_token():
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

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        json_response = response.json()

        # Extract the access_token
        access_token = json_response.get('access_token')

        # Print or use the access_token
        return access_token
    else:
        # Print the error message if the request was not successful
        print(f"Error: {response.status_code}, {response.text}")
        return None
