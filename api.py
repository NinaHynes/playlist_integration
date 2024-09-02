from flask import Flask, jsonify
import json

app = Flask(__name__)

# Load JSON file containing track locations and playlists
with open('track_locations.json', 'r') as file:
    playlists = json.load(file)

# API to get all playlists
@app.route('/api/playlists', methods=['GET'])
def get_all_playlists():
    # Return a list of all playlist names
    playlist_names = [playlist['playlist_name'] for playlist in playlists]
    return jsonify(playlist_names), 200

# API to get details of a specific playlist by name
@app.route('/api/playlists/<string:playlist_name>', methods=['GET'])
def get_playlist_by_name(playlist_name):
    # Find the playlist by name
    playlist = next((p for p in playlists if p['playlist_name'].lower() == playlist_name.lower()), None)
    if playlist:
        return jsonify(playlist), 200
    else:
        return jsonify({'message': 'Playlist not found'}), 404

# API to get the number of tracks in a specific playlist
@app.route('/api/playlists/<string:playlist_name>/count', methods=['GET'])
def get_playlist_track_count(playlist_name):
    # Find the playlist by name
    playlist = next((p for p in playlists if p['playlist_name'].lower() == playlist_name.lower()), None)
    if playlist:
        track_count = len(playlist['tracks'])
        return jsonify({'playlist_name': playlist_name, 'track_count': track_count}), 200
    else:
        return jsonify({'message': 'Playlist not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
