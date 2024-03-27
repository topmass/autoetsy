import requests
import json
import os
import time

# Adjusted to use text-to-image endpoint
host = "http://127.0.0.1:8888"

def text2img(params: dict) -> dict:
    """
    Image Generation without an image prompt.
    """
    # Endpoint adjusted to text-to-image
    result = requests.post(url=f"{host}/v1/generation/text-to-image",
                           data=json.dumps(params),
                           headers={"Content-Type": "application/json"})
    return result.json()

def check_job_status(job_id: str) -> dict:
    """
    Check the status of the image generation job.
    """
    import sys

    # Hide cursor for cleaner output
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

        # Display progress bar for image generation
        job_progress = status.get('job_progress', 0)
        bar_length = 50
        filled_length = int(bar_length * job_progress // 100)
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        sys.stdout.write(f'\rImage generation progress: |{bar}| {job_progress}% Complete')
        sys.stdout.flush()

        if status['job_stage'] in ['COMPLETED', 'FAILED', 'SUCCESS']:
            print("\n")  # Ensure the next print statement is on a new line
            break
        time.sleep(2)

    # Show cursor
    sys.stdout.write('\033[?25h')
    sys.stdout.flush()

    return status

# Read the prompt from 'image_gen_prompt.md'
with open('image_gen_prompt.md', 'r') as file:
    prompt_text = file.read().strip()

params = {
    "prompt": prompt_text,
    "async_process": True,
    "style_selections": ['Fooocus Sharp', 'Artstyle Impressionist'],
    "base_model_name": "juggernautXL_v8Rundiffusion.safetensors",
    "guidance_scale": 5,
    "sharpness": 10,
    "negative_prompt": "unrealistic, saturated, sketch, cartoon, anime, manga, render, watermark, signature, label, artist signature",
    "aspect_ratios_selection": '2000*1500',
    "performance_selection": "Speed",
}

try:
    # Generate the image with text2img function
    job_response = text2img(params)
    if job_response.get('job_id'):
        print("Starting image generation...")
        job_status = check_job_status(job_response['job_id'])
        if job_status.get('job_stage') == 'SUCCESS':
            print("Image generation completed successfully.")
        else:
            print("Text-to-image job did not complete successfully.")
    else:
        print("Failed to initiate text-to-image job.")
except Exception as e:
    print(e)

