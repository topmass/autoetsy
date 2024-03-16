import subprocess
import glob
import os
import sys
import ollama
import time
import requests
from datetime import datetime

# Function to run a script with a filename argument and capture its output
def run_script(script_name, filename):
    result = subprocess.run(['python', script_name, filename], capture_output=True, text=True)
    return result.stdout

# Function to process a single pull_* file
def process_file():
    # Find the first pull_*.html file in the dump folder
    html_files = glob.glob('dump/pull_*.html')
    if html_files:
        html_file = html_files[0]  # Process the first file foundnow
        base_name = os.path.basename(html_file)
        file_name_without_ext = os.path.splitext(base_name)[0]
        
        # Run extracthtml.py for the current file
        extract_output = run_script('extracthtml.py', file_name_without_ext)
        
        # Prepare the filename for the described_image script
        image_file_name = f"extracted_images/{file_name_without_ext}.jpg"
        
        # Initialize a dictionary to store outputs
        outputs = {}
        
        # Running describe_image.py three times and storing outputs
        for i in range(1, 2):
            response = ollama.chat(
                model='llava',
                messages=[
                    {
                        'role': 'user',
                        'content': """For this task, you're to analyze an image of a framed photo. Your description should exclusively detail the content captured within the boundaries of the frame, entirely disregarding the frame itself, any mounting or display methods, and any other external attributes. Focus your analysis on identifying and describing the subjects, setting, mood, art style and thematic elements present in the image content. Pretend the frame is invisible and provide a vivid description of the scene depicted in the photo as if recounting a story or painting a picture with words. Keywords to concentrate on include 'depicted scene,' 'image content,' and 'artwork's narrative.""",
                        'images': [image_file_name],  # Use the dynamically passed image file name
                    },
                ]
            )
            outputs[f'Run {i}'] = response['message']['content']

        # Writing outputs to a markdown file with two line breaks between each
        with open(f'{file_name_without_ext}_described.md', 'w') as file:
            for key, value in outputs.items():
                file.write(f"{value}\n\n")

        # Ollama to generate a new description based on 3 llava outputs and the contents of the described file

        # Read the contents of the described file
        with open(f'{file_name_without_ext}_described.md', 'r') as described_file:
            described_contents = described_file.read()

        # Generate a new description by passing the contents of the described file
        response = ollama.chat(
            model='dolphin-mistral',
            messages=[
                {
                    'role': 'user',
                    'content': f"""{described_contents}
                    The above are a few painting descriptions I'm seeking to refine a prompt for an image generation model to ensure it focuses exclusively on the artistic content of paintings. The aim is to generate descriptions or images that capture the scene depicted in the artwork, including subjects, setting, mood, and narrative elements. It is crucial to omit any references to the print company, the material of the print (e.g., canvas, paper), the type of frame, or how it's displayed. The focus should be solely on the artwork's scene. For example, if the original summary includes 'Printed by XYZ Company on high-quality canvas, framed in a modern black frame, depicting a serene lakeside sunset,' the refined prompt should only describe 'a serene lakeside sunset.' This approach will ensure that the model's output remains focused on the artistic depiction rather than extraneous details. always begin your reply ONLY with "a painting of ..." and then continue describing the artwork """,
                },
            ]
        )

        # Save the Mistral output to a new file as our final output for image generation prompt
        with open(f'{file_name_without_ext}_final.md', 'w') as final_file:
            final_file.write(response['message']['content'])

        print(response['message']['content'])

        print(f"Script execution for {file_name_without_ext} completed. Outputs saved in {file_name_without_ext}_described.md and {file_name_without_ext}_final.md.")
        # Delete the processed HTML file
        os.remove(html_file)
    else:
        print("No pull_* files found in the dump folder.")

    # New functionality to generate and upscale an image based on the final output
    final_output_file = f"{file_name_without_ext}_final.md"
    final_output_text = read_final_output(final_output_file)
    generated_image_path = generate_image_from_text(final_output_text)
    upscaled_image_path = upscale_image(generated_image_path)

    print(f"Generated image saved at {generated_image_path}")
    print(f"Upscaled image saved at {upscaled_image_path}")

def read_final_output(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def generate_image_from_text(prompt):
    date_today = datetime.now().strftime("%Y-%m-%d")
    folder_path = f"focusgen/{date_today}/"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    # Pre-check: Get a list of existing files in the directory before making the API call
    pre_existing_files = set(os.listdir(folder_path))
    
    # API call to generate the image
    url = "http://127.0.0.1:8888/v1/generation/text-to-image"
    params = {
        "prompt": prompt,
        "require_base64": False,
        "async_process": False  # Assuming synchronous processing for simplicity
    }
    response = requests.post(url, json=params)
    if response.status_code == 200:
        print("Image generation initiated successfully.")
        # Monitor the folder for a new file
        return wait_for_image(folder_path, pre_existing_files)
    else:
        raise Exception("Image generation failed", response.text)

def wait_for_image(folder_path, pre_existing_files):
    print("Waiting for the image to be generated...")
    start_time = time.time()
    while True:
        current_files = set(os.listdir(folder_path))
        new_files = current_files - pre_existing_files
        if new_files:
            new_image_path = os.path.join(folder_path, list(new_files)[0])
            print(f"New image detected: {new_image_path}")
            return new_image_path
        # Check for the new file every 0.1 seconds to reduce delay
        time.sleep(0.1)
        # Timeout after 60 seconds to prevent infinite loop
        if time.time() - start_time > 60:
            raise TimeoutError("Image generation timed out.")

def upscale_image(image_path):
    folder_path = os.path.dirname(image_path)
    existing_files = set(os.listdir(folder_path))
    
    url = "http://127.0.0.1:8888/v2/generation/image-upscale-vary"
    files = {'input_image': open(image_path, 'rb')}
    params = {
        "uov_method": "Upscale (2x)",
        "async_process": False
    }
    response = requests.post(url, files=files, data=params)
    if response.status_code != 200:
        raise Exception("Failed to upscale image")
    
    print("Waiting for the upscaled image...")
    while True:
        current_files = set(os.listdir(folder_path))
        new_files = current_files - existing_files
        if new_files:
            upscaled_image_path = os.path.join(folder_path, new_files.pop())
            print(f"Upscaled image detected: {upscaled_image_path}")
            return upscaled_image_path
        time.sleep(1)

# Function to process all pull_* files in the dump folder
def process_all_files():
    while True:
        process_file()
        time.sleep(2)

# Main script
if __name__ == "__main__":
    process_file()