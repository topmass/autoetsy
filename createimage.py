import requests
import json
import base64
from pathlib import Path
import time
import os
import glob
from datetime import datetime
import re
import requests
import json

# The rest of your code remains unchanged

# Vincent diagram example
host = "http://127.0.0.1:8888"

def encode_image_to_base64(image_path: str) -> str:
    """
    Encode the image to base64.
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def find_latest_jpg_image(directory: str) -> str:
    """
    Find the latest (most recently modified) .jpg file in the specified directory.
    """
    list_of_jpg = glob.glob(os.path.join(directory, '*.jpg'))
    if not list_of_jpg:
        raise FileNotFoundError("No .jpg files found in the specified directory.")
    latest_file = max(list_of_jpg, key=os.path.getmtime)
    return latest_file

def text2img(params: dict, image_prompt: str = None) -> dict:
    """
    Image Generation with optional image prompt.
    """
    if image_prompt:
        params['image_prompts'] = [{
            "cn_img": image_prompt,
            "cn_stop": 0.6,
            "cn_weight": 0.6,
            "cn_type": "ImagePrompt"
        }]
    
    result = requests.post(url=f"{host}/v2/generation/text-to-image-with-ip",
                           data=json.dumps(params),
                           headers={"Content-Type": "application/json"})
    return result.json()

def check_job_status(job_id: str, process_type: str = "generation") -> dict:
    import sys
    dot_count = 0  # Initialize dot count for upscaling indication

    # Hide cursor
    sys.stdout.write('\033[?25l')
    sys.stdout.flush()

    while True:
        result = requests.get(url=f"{host}/v1/generation/query-job",
                              params={"job_id": job_id, "require_step_preview": False},
                              timeout=30)
        status = result.json()

        if 'job_stage' not in status:
            print("Unexpected response structure:", status)
            break

        if process_type == "generation":
            # Display progress bar only for image generation
            job_progress = status.get('job_progress', 0)
            bar_length = 50
            filled_length = int(bar_length * job_progress // 100)
            bar = '█' * filled_length + '-' * (bar_length - filled_length)
            sys.stdout.write(f'\rImage generation progress: |{bar}| {job_progress}% Complete')
            sys.stdout.flush()
        else:
            # For upscaling, display a growing trail of dots, resetting visually by overwriting with spaces
            dot_display = '.' * dot_count + ' ' * (3 - dot_count)
            sys.stdout.write(f'\rUpscaling{dot_display}')
            sys.stdout.flush()
            dot_count = (dot_count + 1) % 4

        if status['job_stage'] in ['COMPLETED', 'FAILED', 'SUCCESS']:
            print("\n")  # Ensure the next print statement is on a new line
            break
        time.sleep(2)

    # Show cursor
    sys.stdout.write('\033[?25h')
    sys.stdout.flush()

    return status

def upscale_image_v2(image_url: str, uov_method: str = "Upscale (Fast 2x)") -> dict:
    """
    Upscale the generated image using V2 endpoint.
    """
    params = {
        "input_image": image_url,
        "uov_method": uov_method,
        "async_process": True  # To process the job asynchronously
    }
    response = requests.post(url=f"{host}/v2/generation/image-upscale-vary",
                             data=json.dumps(params),
                             headers={"Content-Type": "application/json"},
                             timeout=300)
    return response.json()

# Read the prompt from 'image_gen_prompt.md'
with open('image_gen_prompt.md', 'r') as file:
    prompt_text = file.read().strip()

try:
    image_directory = 'extracted_images'
    image_path = find_latest_jpg_image(image_directory)
    encoded_image = encode_image_to_base64(image_path)

    params = {
        "prompt": prompt_text,
        "async_process": True,
        "style_selections": ["Artstyle Impressionist",],
        "aspect_ratios_selection": '2100*1500',
        "generation_speed": "fast",  # Added selector for fast generation
    }
    # After generating the image with text2img function, now including an image prompt
    job_response = text2img(params, encoded_image)
    if job_response.get('job_id'):
        print("Starting image generation...")
        job_status = check_job_status(job_response['job_id'], "generation")
        if job_status.get('job_stage') == 'SUCCESS':
            directory_path = Path(f"focusgen/{datetime.now().strftime('%Y-%m-%d')}")
            # Regular expression to match files ending with _<4digits>.png
            pattern = re.compile(r"_\d{4}\.png$")
            # Iterate over all files in the directory matching the pattern
            for file_path in directory_path.iterdir():
                if file_path.is_file() and pattern.search(file_path.name):
                    os.remove(file_path)
                    print(f"Deleted PNG file: {file_path.name}")
            # os remove the last image saved to folder focusgen/{todays_date} ending in .png
            
            print("Image generation completed. Starting upscaling...")
            # Assuming the job_result contains a URL to the generated image
            image_url = job_status.get('job_result', [{}])[0].get('url')
            if image_url:
                # Send the image to the upscale API using V2 endpoint with 1.5x upscale
                upscale_response = upscale_image_v2(image_url, "Upscale (Fast 2x)")
                if upscale_response.get('job_id'):
                    # Check the status of the upscale job with a different process type
                    upscale_status = check_job_status(upscale_response['job_id'], "upscaling")
                    if upscale_status.get('job_stage') == 'SUCCESS':
                        print("Upscaling completed successfully.")
                    else:
                        print("Upscaling did not complete successfully.")
                else:
                    print("Failed to initiate upscaling job.")
            else:
                print("No image URL found in job result.")
        else:
            print("Text-to-image job did not complete successfully.")
    else:
        print("Failed to initiate text-to-image job.")
except FileNotFoundError as e:
    print(e)
