# app.py

from fastapi import FastAPI, UploadFile, HTTPException
from models import LibraryData
from parse_rekordbox import parse_rekordbox_xml
from parse_collection import parse_collection_nml
from parse_library import parse_library_xml



app = FastAPI()

@app.post("/upload-rekordbox", response_model=LibraryData)
async def upload_rekordbox_xml(xml_file: UploadFile):
    if not xml_file.filename.endswith('.xml'):
        raise HTTPException(status_code=400, detail="Only XML files are allowed.")
    
    try:
        return parse_rekordbox_xml(xml_file.file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload-collection", response_model=LibraryData)
async def upload_collection_nml(xml_file: UploadFile):
    if not xml_file.filename.endswith('.nml'):
        raise HTTPException(status_code=400, detail="Only NML files are allowed.")
    
    try:
        return parse_collection_nml(xml_file.file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload-library", response_model=LibraryData)
async def upload_library_xml(xml_file: UploadFile):
    if not xml_file.filename.endswith('.xml'):
        raise HTTPException(status_code=400, detail="Only XML files are allowed.")
    
    try:
        return parse_library_xml(xml_file.file)
    except Exception as e:
        # Log the full error to see what went wrong
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

