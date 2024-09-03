from fastapi import FastAPI, UploadFile, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
import xml.etree.ElementTree as ET

app = FastAPI()

class TrackLocation(BaseModel):
    directory: Optional[str] = None
    file: Optional[str] = None
    volume: Optional[str] = None

class Track(BaseModel):
    track_id: Optional[str] = None
    title: Optional[str] = None
    artist: Optional[str] = None
    album: Optional[str] = None
    location: Optional[str] = None
    bitrate: Optional[int] = None
    duration: Optional[int] = None

class LibraryData(BaseModel):
    tracks: List[Track] = []

def parse_plist_track(track_dict) -> Track:
    """
    Extract track information from the plist XML entry.
    """
    track = Track()
    
    key = None
    for element in track_dict:
        if element.tag == 'key':
            key = element.text
        elif key == "Track ID":
            track.track_id = element.text
        elif key == "Name":
            track.title = element.text
        elif key == "Artist":
            track.artist = element.text
        elif key == "Album":
            track.album = element.text
        elif key == "Location":
            track.location = element.text
        elif key == "Bit Rate":
            try:
                track.bitrate = int(element.text)
            except (ValueError, TypeError):
                track.bitrate = None
        elif key == "Total Time":
            try:
                track.duration = int(element.text)
            except (ValueError, TypeError):
                track.duration = None
    
    return track

@app.post("/upload-xml", response_model=LibraryData)
async def upload_xml(xml_file: UploadFile):
    if not xml_file.filename.endswith('.xml'):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only XML files are allowed.")
    
    try:
        tree = ET.parse(xml_file.file)
        root = tree.getroot()

        # Locate the "Tracks" dictionary
        tracks = []
        tracks_dict = None
        
        for dict_elem in root.iter('dict'):
            for i, key_elem in enumerate(dict_elem):
                if key_elem.tag == 'key' and key_elem.text == "Tracks":
                    # The next element after the "Tracks" key should be the dict containing tracks
                    tracks_dict = list(dict_elem)[i + 1]
                    break
            if tracks_dict is not None:
                break

        if tracks_dict is not None and tracks_dict.tag == 'dict':
            # Now process each track within the "Tracks" dictionary
            for track_key_elem in tracks_dict.findall('key'):
                # Each key is followed by a dict that contains track information
                next_elem_index = list(tracks_dict).index(track_key_elem) + 1
                track_dict = list(tracks_dict)[next_elem_index]
                if track_dict.tag == 'dict':
                    tracks.append(parse_plist_track(track_dict))
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tracks not found in the XML file.")
        
        library_data = LibraryData(tracks=tracks)
        return library_data
    
    except ET.ParseError as parse_error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"XML Parse Error: {str(parse_error)}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected Error: {str(e)}")






