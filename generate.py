import replicate
import os
import re
import requests  # Import the requests library

# Function to find the latest pull_*_final.md file and extract its number
def find_latest_pull_file_number():
    pull_files = [f for f in os.listdir('.') if re.match(r'pull_\d+_final.md', f)]
    if not pull_files:
        raise FileNotFoundError("No pull_*_final.md files found.")
    latest_file = max(pull_files, key=os.path.getctime)
    match = re.search(r'pull_(\d+)_final.md', latest_file)
    if match:
        return match.group(1)
    else:
        raise ValueError("Could not extract number from the latest pull file.")

# Extract the number from the latest pull file
pull_number = find_latest_pull_file_number()

# Read the prompt from the latest pull file
prompt_file_path = f'pull_{pull_number}_final.md'
with open(prompt_file_path, 'r') as file:
    prompt_content = file.read()

# Run the replicate model with the extracted prompt
output = replicate.run(
    "fofr/latent-consistency-model:683d19dc312f7a9f0428b04429a9ccefd28dbf7785fef083ad5cf991b65f406f",
    input={
        "width": 1920,
        "height": 1080,
        "prompt": prompt_content,
        "num_images": 1,
        "guidance_scale": 8,
        "archive_outputs": False,
        "prompt_strength": 0.6,
        "sizing_strategy": "width/height",
        "lcm_origin_steps": 50,
        "canny_low_threshold": 100,
        "num_inference_steps": 4,
        "canny_high_threshold": 200,
        "control_guidance_end": 1,
        "control_guidance_start": 0,
        "controlnet_conditioning_scale": 2
    }
)

# Assuming the output contains a URL to the image under the 'image_url' key
image_url = output['image_url']

# Use requests to fetch the image from the URL
response = requests.get(image_url)
if response.status_code == 200:
    # Save the fetched image to the specified output path
    output_image_path = f'New_Listings/pull_{pull_number}.png'
    with open(output_image_path, 'wb') as file:
        file.write(response.content)
    print(f"Image saved to {output_image_path}")
else:
    print(f"Failed to download the image. Status code: {response.status_code}")
