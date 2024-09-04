import xml.etree.ElementTree as ET
from models import Track, Playlist, LibraryData

def parse_library_xml(file) -> LibraryData:
    try:
        tree = ET.parse(file)
        root = tree.getroot()

        # Dictionary to store track details
        track_dict = {}
        playlists = []

        # Locate the "Tracks" dictionary
        tracks_dict = None
        for dict_elem in root.iter('dict'):
            for i, key_elem in enumerate(dict_elem):
                if key_elem.tag == 'key' and key_elem.text == "Tracks":
                    # The next element after "Tracks" should be the dict containing track details
                    tracks_dict = list(dict_elem)[i + 1]
                    break
            if tracks_dict is not None:
                break

        if tracks_dict is not None and tracks_dict.tag == 'dict':
            # Process each track within the "Tracks" dictionary
            track_elements = list(tracks_dict)
            for i in range(0, len(track_elements), 2):
                track_key_elem = track_elements[i]
                track_data_elem = track_elements[i + 1] if i + 1 < len(track_elements) else None

                if track_key_elem.tag == 'key' and track_data_elem is not None and track_data_elem.tag == 'dict':
                    track_info = {}
                    track_id = None
                    key_name = None
                    # Extract all key-value pairs for each track
                    track_data = list(track_data_elem)
                    for j in range(0, len(track_data), 2):
                        key = track_data[j]
                        value = track_data[j + 1] if j + 1 < len(track_data) else None

                        if key.tag == 'key':
                            key_name = key.text
                            if key_name == "Track ID" and value is not None:
                                track_id = value.text
                            elif key_name == "Name" and value is not None:
                                track_info['name'] = value.text
                            elif key_name == "Artist" and value is not None:
                                track_info['artist'] = value.text
                            elif key_name == "Album" and value is not None:
                                track_info['album'] = value.text
                            elif key_name == "Location" and value is not None:
                                track_info['location'] = value.text
                            elif key_name == "Bit Rate" and value is not None:
                                track_info['bitrate'] = int(value.text) if value.text else None
                            elif key_name == "Total Time" and value is not None:
                                track_info['duration'] = int(value.text) if value.text else None

                    # Only add the track if we successfully captured its ID and essential details
                    if track_id and track_info:
                        track_dict[track_id] = Track(
                            track_id=track_id,
                            name=track_info.get('name'),
                            artist=track_info.get('artist'),
                            album=track_info.get('album'),
                            location=track_info.get('location'),
                            bitrate=track_info.get('bitrate'),
                            duration=track_info.get('duration')
                        )

        # Locate Playlists (if available)
        found_playlists_section = False
        for dict_elem in root.iter('dict'):
            for key_elem in dict_elem.findall('key'):
                if key_elem.text == "Playlists":
                    found_playlists_section = True
                    print("Found Playlists section")
                    playlists_array = dict_elem.find('array')
                    for playlist_dict in playlists_array.findall('dict'):
                        playlist_name = None
                        playlist_tracks = []

                        # Extract playlist name and track IDs
                        playlist_elements = list(playlist_dict)
                        for k in range(0, len(playlist_elements), 2):
                            playlist_key = playlist_elements[k]
                            playlist_value = playlist_elements[k + 1] if k + 1 < len(playlist_elements) else None

                            if playlist_key.tag == 'key' and playlist_key.text == "Name" and playlist_value is not None:
                                playlist_name = playlist_value.text
                            if playlist_key.tag == 'array':
                                # Extract track IDs from playlist
                                for track_id_elem in playlist_key.findall('dict'):
                                    for track_key_elem in track_id_elem:
                                        if track_key_elem.tag == 'key' and track_key_elem.text == "Track ID":
                                            track_id = track_key_elem.getnext().text
                                            if track_id in track_dict:
                                                playlist_tracks.append(track_dict[track_id])

                        if playlist_tracks and playlist_name:
                            playlists.append(Playlist(playlist_name=playlist_name, tracks=playlist_tracks))

        if not found_playlists_section:
            print("No Playlists section found in the XML file")

        return LibraryData(playlists=playlists, tracks=list(track_dict.values()))

    except ET.ParseError as parse_error:
        raise ValueError(f"XML Parse Error: {str(parse_error)}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise ValueError(f"An error occurred: {str(e)}")
