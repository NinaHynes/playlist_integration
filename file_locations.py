import json

# Load the JSON file
with open('rekordbox_playlists.json', 'r') as file:
    playlists = json.load(file)

# Create a list to store the extracted file paths
file_paths = []

# Iterate through playlists and extract track locations
for playlist in playlists:
    playlist_name = playlist.get('playlist_name')
    for track in playlist.get('tracks', []):
        location = track.get('location')
        if location:
            file_paths.append({
                'playlist_name': playlist_name,
                'track_name': track.get('name'),
                'location': location
            })

# Save the file paths to a CSV file (or print them out)
with open('track_locations.csv', 'w') as output_file:
    output_file.write("Playlist Name,Track Name,Location\n")
    for entry in file_paths:
        output_file.write(f"{entry['playlist_name']},{entry['track_name']},{entry['location']}\n")

print("File paths have been saved to 'track_locations.csv'")
