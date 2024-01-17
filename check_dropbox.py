import requests
import json
import dropbox_oauth





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

if __name__ == "__main__":
    dropbox_api_key =  dropbox_oauth.get_access_token()
    all_files_in_folder(dropbox_api_key)