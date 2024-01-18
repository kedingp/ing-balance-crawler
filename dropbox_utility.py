import requests
import json
import dropbox
import os
import csv

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

def all_files_in_folder(access_token):
    url = "https://api.dropboxapi.com/2/files/list_folder"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    data = {
        "path": ""
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

        # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        json_response = response.json()

        # Extract file names from the list of entries
        file_names = [entry.get('name') for entry in json_response.get('entries', []) if entry.get('.tag') == 'file']
        return file_names

    else:
        # Print the error message if the request was not successful
        print(f"Error: {response.status_code}, {response.text}")
        return None


def download_file(dropbox_access_token, dropbox_file_path, local_file_path):
    dbx = dropbox.Dropbox(dropbox_access_token)
    # Get the current working directory
    current_directory = os.getcwd()

    # Full local file path
    full_local_path = os.path.join(current_directory, local_file_path)
    dbx.files_download_to_file(local_file_path, dropbox_file_path)

    print(f"Data from '{dropbox_file_path}' written successfully to '{full_local_path}'.")


def upload_file(access_token, local_file_path, dropbox_file_path):
    dbx = dropbox.Dropbox(access_token)
    with open(local_file_path, 'rb') as local_file:
        dbx.files_upload(local_file.read(), dropbox_file_path, mode=dropbox.files.WriteMode('overwrite'))

if __name__ == "__main__":
    dropbox_api_key = get_access_token()
    csv_file_path = 'kontostaende.csv'
    with open(csv_file_path, 'w', newline='') as csvfile:
        fieldnames = ['id', 'date', 'bank account', 'balance']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

