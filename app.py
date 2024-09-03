from flask import Flask, request, jsonify
import xml.etree.ElementTree as ET

app = Flask(__name__)

def parse_rekordbox_xml(file):
    try:
        tree = ET.parse(file)
        root = tree.getroot()

        # Step 1: Extract all tracks from the COLLECTION section
        track_dict = {}
        for track in root.findall(".//COLLECTION/TRACK"):
            track_id = track.get('TrackID')
            if track_id:
                track_info = {
                    'name': track.get('Name'),
                    'artist': track.get('Artist'),
                    'album': track.get('Album'),
                    'location': track.get('Location'),  # Include location
                    'genre': track.get('Genre'),
                    'bitrate': track.get('BitRate'),
                    'sample_rate': track.get('SampleRate'),
                    'duration': track.get('TotalTime'),
                    'bpm': track.get('AverageBpm')
                }
                track_dict[track_id] = track_info

        # Step 2: Extract playlists and match them with tracks
        playlists = []

        # If the XML contains a PLAYLISTS section
        playlists_section = root.find(".//PLAYLISTS")
        if playlists_section is not None:
            for node in playlists_section.findall(".//NODE"):
                playlist_name = node.get('Name')

                # Skip the "ROOT" node
                if playlist_name == "ROOT":
                    continue

                playlist_tracks = []

                for track_node in node.findall(".//TRACK"):
                    track_id = track_node.get('Key')
                    if track_id and track_id in track_dict:
                        playlist_tracks.append(track_dict[track_id])

                if playlist_tracks:
                    playlists.append({
                        'playlist_name': playlist_name,
                        'tracks': playlist_tracks
                    })
        else:
            # Handle the case for NODE elements elsewhere in the XML
            for node in root.findall(".//NODE"):
                playlist_name = node.get('Name')

                # Skip the "ROOT" node
                if playlist_name == "ROOT":
                    continue

                playlist_tracks = []

                for track_node in node.findall(".//TRACK"):
                    track_id = track_node.get('Key')
                    if track_id and track_id in track_dict:
                        playlist_tracks.append(track_dict[track_id])

                if playlist_tracks:
                    playlists.append({
                        'playlist_name': playlist_name,
                        'tracks': playlist_tracks
                    })

        return playlists if playlists else "No playlists found."

    except ET.ParseError as parse_error:
        return f"XML Parse Error: {str(parse_error)}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

@app.route('/get_rekordbox_playlists', methods=['POST'])
def get_rekordbox_playlists():
    if 'xml_file' in request.files:
        xml_file = request.files['xml_file']
        if xml_file.filename.endswith('.xml'):
            try:
                playlists = parse_rekordbox_xml(xml_file)
                return jsonify(playlists), 200
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        else:
            return jsonify({'error': 'Only XML files are allowed.'}), 400
    else:
        return jsonify({'error': 'No file provided.'}), 400

if __name__ == '__main__':
    app.run(debug=True)
