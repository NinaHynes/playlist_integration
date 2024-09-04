import xml.etree.ElementTree as ET
from models import Track, Playlist, LibraryData

def extract_track_info(entry) -> Track:
    """
    Extracts track information including metadata and location from an ENTRY element.
    """
    location = entry.find('LOCATION')
    info = entry.find('INFO')
    tempo = entry.find('TEMPO')
    album = entry.find('ALBUM')

    return Track(
        track_id=entry.get('AUDIO_ID'),
        name=entry.get('TITLE'),
        artist=entry.get('ARTIST'),
        album=album.get('TITLE') if album is not None else None,
        location=location.get('FILE') if location is not None else None,
        bitrate=int(info.get('BITRATE')) if info is not None and info.get('BITRATE') is not None else None,
        duration=int(info.get('PLAYTIME')) if info is not None and info.get('PLAYTIME') is not None else None,
        bpm=float(tempo.get('BPM')) if tempo is not None and tempo.get('BPM') is not None else None
    )

def get_track_by_id(track_id, track_collection):
    """
    Finds the track in the collection by AUDIO_ID.
    """
    for track in track_collection:
        if track.get('AUDIO_ID') == track_id:
            return track
    return None

def extract_playlists(root, track_collection) -> list[Playlist]:
    """
    Extracts playlist names and their tracks from the NML structure.
    """
    playlists = []
    
    for playlist in root.findall(".//NODE[@TYPE='PLAYLIST']"):
        playlist_name = playlist.get('NAME')
        playlist_tracks = []
        
        for entry_ref in playlist.findall(".//ENTRY"):
            track_id = entry_ref.get('AUDIO_ID')
            track = get_track_by_id(track_id, track_collection)
            if track:
                playlist_tracks.append(extract_track_info(track))

        playlists.append(Playlist(playlist_name=playlist_name, tracks=playlist_tracks))

    return playlists

def parse_collection_nml(file) -> LibraryData:
    try:
        tree = ET.parse(file)
        root = tree.getroot()

        # Extract tracks from COLLECTION
        track_collection = root.findall(".//COLLECTION/ENTRY")
        tracks = [extract_track_info(entry) for entry in track_collection]

        # Extract playlists and match with tracks
        playlists = extract_playlists(root, track_collection)

        # Return uniform response
        return LibraryData(playlists=playlists, tracks=tracks)

    except ET.ParseError as parse_error:
        raise ValueError(f"XML Parse Error: {str(parse_error)}")
    except Exception as e:
        raise ValueError(f"An error occurred: {str(e)}")
