import os
import shutil
from datetime import datetime
import requests
import json
import base64

# Removed the get_specific_styles function as it's no longer needed due to the removal of the API call to the styles endpoint.

# Determine today's date and construct the folder path
today_date = datetime.now().strftime("%Y-%m-%d")
folder_path = f"C:\\code\\fooocus\\Fooocus\\outputs\\{today_date}"

# Ensure the folder exists
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Define the API endpoint, host, and make the API call with hardcoded style selections
host = "http://127.0.0.1:8888"
endpoint = "/v1/generation/text-to-image"
url = f"{host}{endpoint}"
params = {
    "prompt": "medieval castle",
    "require_base64": True,
    "async_process": False,
    "style_selections": ["Fooocus Enhance", "Fooocus V2", "Artstyle Impressionist"]  # Hardcoded style selections
}
response = requests.post(url, data=json.dumps(params), headers={"Content-Type": "application/json"})
response_data = response.json()

# Save the image to the date-specific folder
if 'base64' in response_data:
    image_data = response_data['base64']
    image_bytes = base64.b64decode(image_data)
    image_path = os.path.join(folder_path, "medieval_castle.png")
    with open(image_path, "wb") as image_file:
        image_file.write(image_bytes)
    print("Image saved successfully to date-specific folder.")
else:
    print("No image data found in the response or the process is asynchronous.")

# Find the most recent image in the folder
files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.png')]
most_recent_file = max(files, key=os.path.getmtime)

# Move the most recent image to "New_Listings"
new_listings_dir = os.path.join(os.path.dirname(__file__), "New_Listings")
if not os.path.exists(new_listings_dir):
    os.makedirs(new_listings_dir)
shutil.move(most_recent_file, os.path.join(new_listings_dir, os.path.basename(most_recent_file)))
print(f"Most recent image moved to {new_listings_dir}.")