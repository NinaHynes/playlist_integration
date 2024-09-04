# models.py

from pydantic import BaseModel
from typing import List, Optional

# Define the Track model
class Track(BaseModel):
    track_id: Optional[str] = None
    name: Optional[str] = None
    artist: Optional[str] = None
    album: Optional[str] = None
    location: Optional[str] = None
    genre: Optional[str] = None
    bitrate: Optional[int] = None
    sample_rate: Optional[int] = None
    duration: Optional[int] = None
    bpm: Optional[float] = None

# Define the Playlist model
class Playlist(BaseModel):
    playlist_name: Optional[str] = None
    tracks: List[Track] = []

# Define the LibraryData model for a uniform response
class LibraryData(BaseModel):
    playlists: List[Playlist] = []
    tracks: List[Track] = []
