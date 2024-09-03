from flask import Flask, request, jsonify
import xml.etree.ElementTree as ET

app = Flask(__name__)

def extract_track_info(entry):
    """
    Extracts track information including metadata and location from an ENTRY element.
    """
    location = entry.find('LOCATION')
    info = entry.find('INFO')
    tempo = entry.find('TEMPO')
    album = entry.find('ALBUM')

    track_info = {
        'title': entry.get('TITLE'),
        'artist': entry.get('ARTIST'),
        'album': album.get('TITLE') if album is not None else None,
        'location': {
            'directory': location.get('DIR') if location is not None else None,
            'file': location.get('FILE') if location is not None else None,
            'volume': location.get('VOLUME') if location is not None else None
        },
        'metadata': {
            'bitrate': info.get('BITRATE') if info is not None else None,
            'key': info.get('KEY') if info is not None else None,
            'playcount': info.get('PLAYCOUNT') if info is not None else None,
            'playtime': info.get('PLAYTIME') if info is not None else None,
            'bpm': tempo.get('BPM') if tempo is not None else None,
            'last_played': info.get('LAST_PLAYED') if info is not None else None,
        }
    }
    return track_info

def get_track_by_id(track_id, track_collection):
    """
    Finds the track in the collection by AUDIO_ID.
    """
    for track in track_collection:
        if track.get('AUDIO_ID') == track_id:
            return track
    return None

def extract_playlists(root, track_collection):
    """
    Extracts playlist names and their tracks from the NML structure.
    """
    playlists = []
    
    for playlist in root.findall(".//NODE[@TYPE='PLAYLIST']"):
        playlist_info = {
            'name': playlist.get('NAME'),
            'tracks': []
        }
        for entry_ref in playlist.findall(".//ENTRY"):
            track_id = entry_ref.get('AUDIO_ID')
            track = get_track_by_id(track_id, track_collection)
            if track:
                location = track.find('LOCATION')
                playlist_info['tracks'].append({
                    'title': track.get('TITLE'),
                    'artist': track.get('ARTIST'),
                    'location': {
                        'directory': location.get('DIR') if location is not None else None,
                        'file': location.get('FILE') if location is not None else None,
                        'volume': location.get('VOLUME') if location is not None else None
                    }
                })
        playlists.append(playlist_info)
    return playlists

@app.route('/get_library_data', methods=['POST'])
def get_library_data():
    if 'xml_file' in request.files:
        xml_file = request.files['xml_file']
        if xml_file.filename.endswith('.nml'):
            try:
                tree = ET.parse(xml_file)
                root = tree.getroot()
                
                # Extracting tracks with metadata and location
                tracks = []
                track_collection = root.findall(".//COLLECTION/ENTRY")
                for entry in track_collection:
                    tracks.append(extract_track_info(entry))
                
                # Extracting playlist names and their tracks, including locations
                playlists = extract_playlists(root, track_collection)
                
                # Construct the final output
                library_data = {
                    'tracks': tracks,
                    'playlists': playlists
                }
                
                # Return the data as a JSON response
                return jsonify(library_data), 200
            
            except ET.ParseError as parse_error:
                return jsonify({'error': f"XML Parse Error: {str(parse_error)}"}), 500
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        else:
            return jsonify({'error': 'Only NML files are allowed.'}), 400
    else:
        return jsonify({'error': 'No file provided.'}), 400

if __name__ == '__main__':
    app.run(debug=True)

