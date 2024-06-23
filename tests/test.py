import requests
import base64

url = "http://127.0.0.1:8000/createPackage"

# List of file paths
file_paths = ["demo_data/rand26.pdf"]

# Prepare the files for the request
files = [("files", (file_path, open(file_path, "rb"), "application/pdf")) for file_path in file_paths]

# Prepare the data for the request
data = {
    "name": "Test Package"
}

response = requests.post(url, data=data, files=files)

print(response.status_code)
print(response.json())
