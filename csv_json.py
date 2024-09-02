import csv
import json

# Load the CSV file
csv_file = 'track_locations.csv'
json_file = 'track_locations.json'

data = []
with open(csv_file, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        data.append(row)

# Save as a JSON file
with open(json_file, 'w') as f:
    json.dump(data, f, indent=4)

print(f"Data from {csv_file} has been converted to {json_file}")
