import requests
import json

# Load the JSON data
with open('track_locations.json', 'r') as f:
    data = json.load(f)

# Define Kopf API endpoint and authentication details
api_url = 'https://api.kopf.com/v1/tasks'  # Example endpoint
headers = {
    'Authorization': 'Bearer YOUR_ACCESS_TOKEN',
    'Content-Type': 'application/json'
}

# Iterate through the data and send it to Kopf
for track in data:
    task_payload = {
        "title": f"Track: {track['Track Name']}",
        "description": f"Location: {track['Location']}\nPlaylist: {track['Playlist Name']}",
        # Add other fields as needed
    }

    response = requests.post(api_url, headers=headers, json=task_payload)

    if response.status_code == 201:
        print(f"Task created successfully for track: {track['Track Name']}")
    else:
        print(f"Failed to create task for track: {track['Track Name']} - {response.content}")
