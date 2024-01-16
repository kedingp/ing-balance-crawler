import requests
import json
import os


dropbox_api_key = os.environ.get('DROPBOX_API_KEY')



url = "https://api.dropboxapi.com/2/files/list_folder"

headers = {
    "Authorization": f"Bearer {dropbox_api_key}",
    "Content-Type": "application/json"
}

data = {
    "path": ""
}

r = requests.post(url, headers=headers, data=json.dumps(data))
print(r.status_code)

print("Response Content:")
print(r.text)