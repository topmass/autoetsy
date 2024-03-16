import requests
import json
import base64
from pathlib import Path
import time

import requests
import json

# Vincent diagram example
host = "http://127.0.0.1:8888"

def text2img(params: dict) -> dict:
    """
    Image Generation
    """
    
    result = requests.post(url=f"{host}/v1/generation/text-to-image",
                           data=json.dumps(params),
                           headers={"Content-Type": "application/json"})
    return result.json()

def check_job_status(job_id: str) -> dict:
    while True:
        result = requests.get(url=f"{host}/v1/generation/query-job",
                              params={"job_id": job_id, "require_step_preview": False},
                              timeout=30)
        status = result.json()
        
        # Check if 'job_stage' key exists in the response
        if 'job_stage' not in status:
            print("Unexpected response structure:", status)
            break  # or handle it differently based on your needs
        
        if status['job_stage'] in ['COMPLETED', 'FAILED', 'SUCCESS']:
            return status
        time.sleep(5)  # Adjust sleep time as needed

def upscale_image(image_url: str, uov_method: str = "Upscale (2x)") -> dict:
    """
    Upscale the generated image.
    """
    # Assuming the image is publicly accessible via URL, we directly use the URL.
    # If the image is not publicly accessible, you would need to download it and then upload it as part of the request.
    params = {
        "input_image": image_url,
        "uov_method": uov_method,
        "async_process": True  # To process the job asynchronously
    }
    response = requests.post(url=f"{host}/v1/generation/image-upscale-vary",
                             data=json.dumps(params),
                             headers={"Content-Type": "application/json"})
    return response.json()

# Read the prompt from 'image_gen_prompt.md'
with open('image_gen_prompt.md', 'r') as file:
    prompt_text = file.read().strip()

params = {
    "prompt": prompt_text,
    "async_process": True,
    "style_selections": ["Artstyle Impressionist", "Fooocus V2"]
}
# After generating the image with text2img function
job_response = text2img(params)
if job_response.get('job_id'):
    job_status = check_job_status(job_response['job_id'])
    if job_status.get('job_stage') == 'SUCCESS':
        # Assuming the job_result contains a URL to the generated image
        image_url = job_status.get('job_result', [{}])[0].get('url')
        if image_url:
            # Send the image to the upscale API
            upscale_response = upscale_image(image_url)
            if upscale_response.get('job_id'):
                # Check the status of the upscale job
                upscale_status = check_job_status(upscale_response['job_id'])
                print(upscale_status)
            else:
                print("Failed to initiate upscale job.")
        else:
            print("No image URL found in job result.")
    else:
        print("Text-to-image job did not complete successfully.")
else:
    print("Failed to initiate text-to-image job.")

