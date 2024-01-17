import requests
import json
import dropbox_oauth
import dropbox
import os
import csv

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


def download(dropbox_access_token, dropbox_file_path, local_file_path):
    dbx = dropbox.Dropbox(dropbox_access_token)
    # Get the current working directory
    current_directory = os.getcwd()

    # Full local file path
    full_local_path = os.path.join(current_directory, local_file_path)

    # Download the file from Dropbox and append to it
    with open(full_local_path, 'w', encoding='utf-8') as local_file:
        _, response = dbx.files_download(dropbox_file_path)
        local_file.write(response.content.decode('utf-8'))

    print(f"Data from '{dropbox_file_path}' written successfully to '{full_local_path}'.")



def get_file(access_token, file_path):
        # Initialize Dropbox client
    dbx = dropbox.Dropbox(access_token)
    local_file_path = file_path.strip('/')

    # Download the file from Dropbox
    try:
        with open(local_file_path, 'wb') as local_file:
            _, response = dbx.files_download(file_path)
            local_file.write(response.content)
        print(f"File '{file_path}' downloaded successfully to '{local_file_path}'.")
    except dropbox.exceptions.HttpError as e:
        print(f"Error downloading file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        pass

def upload_file(access_token):
    pass

if __name__ == "__main__":
    dropbox_api_key =  dropbox_oauth.get_access_token()
    dbx = dropbox.Dropbox(dropbox_api_key)
    csv_file_path = 'kontostaende.csv'
    with open(csv_file_path, 'w', newline='') as csvfile:
        fieldnames = ['id', 'date', 'bank account', 'balance']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
    # Upload the modified file back to Dropbox
    with open(csv_file_path, 'rb') as local_file:
        dbx.files_upload(local_file.read(), '/kontostaende.csv', mode=dropbox.files.WriteMode('overwrite'))

    # file_path = 'existing.csv'
    # if file_path in all_files_in_folder(dropbox_api_key):
    #     print("file is available. start download")
    #     dropbox_path = '/' + file_path
    #     download(dropbox_api_key, dropbox_path, file_path)
    # else:
    #     print("File does not exist")
