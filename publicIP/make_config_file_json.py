import json

data = {}

data["config"] = []
data["config"].append({
    "name": "Name",
    "description": "Description",
    "location": "Location",
    "url_token": "Url_token",
    "file_name_data_saved": "Name_file"
})

with open('config.json', 'w') as file:
    json.dump(data, file, indent=4)