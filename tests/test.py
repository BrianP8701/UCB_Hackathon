import requests
import base64

url = "http://127.0.0.1:8000/createPackage"

# List of file paths
file_paths = ["data/raw/pdfs/nar_realtor/nar_realtor_8.pdf"]

# Read and encode files
encoded_files = []
for file_path in file_paths:
    with open(file_path, "rb") as file:
        encoded_files.append(base64.b64encode(file.read()).decode('utf-8'))  # Encode to base64 and convert to string

# Prepare the data for the request
data = {
    "name": "Test Package",
    "files": encoded_files
}


response = requests.post(url, json=data)

print(response.status_code)
print(response.json())
