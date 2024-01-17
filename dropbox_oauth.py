#!/usr/bin/env python3
import os
import dropbox
from dropbox import DropboxOAuth2FlowNoRedirect

'''
This example walks through a basic oauth flow using the existing long-lived token type
Populate your app key and app secret in order to run this locally
'''
APP_KEY = os.environ.get('DROPBOX_KEY')
APP_SECRET = os.environ.get('DROPBOX_SECRET')

auth_flow = DropboxOAuth2FlowNoRedirect(APP_KEY, APP_SECRET, token_access_type="offline")

authorize_url = auth_flow.start()
auth_code = os.environ.get("DROPBOX_AUTH_CODE")

try:
    oauth_result = auth_flow.finish(auth_code)
except Exception as e:
    print('Error: %s' % (e,))
    exit(1)

print(f"Access token: {oauth_result.access_token}")
print(f"Refresh token: {oauth_result.refresh_token}")

with dropbox.Dropbox(oauth2_access_token=oauth_result.access_token) as dbx:
    dbx.users_get_current_account()
    print("Successfully set up client!")