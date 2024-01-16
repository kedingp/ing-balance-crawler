import requests
import json

import os


dropbox_api_key = os.environ.get('DROPBOX_API_KEY')

def check_file_existence(token, file_path):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    }

    data = {
        'path': file_path,
        'include_media_info': False,
        'include_deleted': False,
        'include_has_explicit_shared_members': False,
        'include_mounted_folders': True,
    }

    response = requests.post(
        'https://api.dropboxapi.com/2/files/get_metadata',
        headers=headers,
        data=json.dumps(data)
    )
    print(f"Status code: {response.status_code}")
    return response.status_code == 200

# Replace 'YOUR_DROPBOX_TOKEN' with your actual Dropbox access token
dropbox_token = 'YOUR_DROPBOX_TOKEN'

# Replace '/path/to/existing.csv' with the actual path and filename you want to check
file_path_to_check = './existing.csv'

if check_file_existence(dropbox_api_key, file_path_to_check):
    print(f'The file {file_path_to_check} exists in Dropbox.')
else:
    print(f'The file {file_path_to_check} does not exist in Dropbox.')
