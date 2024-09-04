import xml.etree.ElementTree as ET

# Load your original XML file using the correct path
tree = ET.parse('/home/dci-student/Documents/rekordbox/itunes/recordbox (orig).xml')
root = tree.getroot()

# Create the root element for the new XML
dj_playlists = ET.Element('DJ_PLAYLISTS', Version="1.0.0")

# Create the COLLECTION element
collection = ET.SubElement(dj_playlists, 'COLLECTION', Entries="0")
track_ids_added = set()

# Create the PLAYLISTS element
playlists = ET.SubElement(dj_playlists, 'PLAYLISTS')

# Iterate over each NODE (playlist) in the original XML
for node in root.findall(".//NODE"):
    playlist_name = node.get('Name')
    
    # Create a new NODE in the smaller XML
    new_node = ET.SubElement(playlists, 'NODE', Name=playlist_name)
    
    # Find the first TRACK in the playlist
    track_node = node.find(".//TRACK")
    if track_node is not None:
        track_id = track_node.get('Key')
        
        # Add the TRACK reference to the new NODE
        ET.SubElement(new_node, 'TRACK', Key=track_id)
        
        # If the track has not been added yet, add it to the COLLECTION
        if track_id not in track_ids_added:
            track = root.find(f".//COLLECTION/TRACK[@TrackID='{track_id}']")
            if track is not None:
                collection.append(track)
                track_ids_added.add(track_id)

# Update the Entries count in COLLECTION
collection.set('Entries', str(len(track_ids_added)))

# Save the smaller XML to a file
smaller_tree = ET.ElementTree(dj_playlists)
output_path = "/home/dci-student/Documents/rekordbox/itunes/small_rekordbox_with_exact_names.xml"
smaller_tree.write(output_path, encoding="utf-8", xml_declaration=True)

print(f"Smaller XML file created: {output_path}")
