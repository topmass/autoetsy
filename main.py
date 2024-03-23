import subprocess
import glob
import os
import sys
import ollama
import time
import requests
from datetime import datetime
import asyncio
import json
import subprocess
import shutil
import re  # Import regular expressions module

# Global flag to indicate if the Mistral model's response has been printed
mistral_response_printed = False
focusgen_response_printed = False
local_model = 'orca-mini'
today_date = datetime.today().strftime('%Y-%m-%d')

# Function to run a script with a filename argument and capture its output
def run_script(script_name, filename):
    result = subprocess.run(['python', script_name, filename], capture_output=True, text=True)
    return result.stdout

    print("Pull File Detected! Extracting Product Image, Product Tags and Title.")

# Function to process a single pull_* file
def process_file():
    global mistral_response_printed
    global html_file  # Added to make html_file accessible for create_folder_for_export
    global base_name  # Declare base_name as a global variable

    # Find the first pull_*.html file in the dump folder
    html_files = glob.glob('dump/pull_*.html')
    if html_files:
        html_file = html_files[0]  # Process the first file found
        base_name = os.path.splitext(os.path.basename(html_file))[0]  # Set the global base_name variable without the file extension
        
        # Run extracthtml.py for the current file
        extract_output = run_script('extracthtml.py', base_name)
        
        # Prepare the filename for the described_image script
        image_file_name = f"extracted_images/{base_name}.jpg"
        
        # Initialize a dictionary to store outputs
        outputs = {}

        print("Text and product image saved.")

        print("Using LLava model to describe Product Image. Please Wait..")
        
        # Running describe_image.py three times and storing outputs
        for i in range(1, 2):
            response = ollama.chat(
                model='llava',
                keep_alive=0,
                messages=[
                    {
                        'role': 'user',
                        'content': """For this task, you're to analyze an image of a framed photo. Your description should exclusively detail the content captured within the boundaries of the frame, entirely disregarding the frame itself, any mounting or display methods, and any other external attributes. Focus your analysis on identifying and describing the subjects, setting, mood, art style and thematic elements present in the image content. Pretend the frame is invisible and provide a vivid description of the scene depicted in the photo as if recounting a story or painting a picture with words. Keywords to concentrate on include 'depicted scene,' 'image content,' and 'artwork's narrative.""",
                        'images': [image_file_name],  # Use the dynamically passed image file name
                    },
                ]
            )
            outputs[f'Run {i}'] = response['message']['content']

        # Writing outputs to a markdown file named pull_image_described.md, overwriting each time
        with open('pull_image_described.md', 'w') as file:
            for key, value in outputs.items():
                file.write(f"{value}\n\n")

                print(f"Image Described. Sending to {local_model} for image generation prompt. Please wait..")

        # Read the contents of the described file
        with open('pull_image_described.md', 'r') as described_file:
            described_contents = described_file.read()

        # Generate a new description by passing the contents of the described file
        response = ollama.chat(
            model=(local_model),
            keep_alive=0,
            messages=[
                {
                    'role': 'user',
                    'content': f"{described_contents}",
                },
                {
                    'role': 'system',
                    'content': "The following is a painting description. I'm seeking to refine a prompt for an image generation model to ensure it focuses exclusively on the artistic content of paintings. The aim is to generate a description or images that capture the scene depicted in the artwork, including subjects, setting, mood, and narrative elements. It is crucial to omit any references to the print company, the material of the print (e.g., canvas, paper), the type of frame, or how it's displayed. The focus should be solely on the artwork's scene. For example, if the original summary includes 'Printed by XYZ Company on high-quality canvas, framed in a modern black frame, depicting a serene lakeside sunset,' the refined prompt should only describe 'a serene lakeside sunset.' This approach will ensure that the model's output remains focused on the artistic depiction rather than extraneous details. always begin your reply ONLY with \"an impressionistic, vintage style oil painting with a subdued, earthy color scheme. The technique should convey texture and dimension, ...\" and then continue describing the artwork (always be consice in your description and only one short paragraph, no line breaks)",
                },
            ]
        )

        # Save the Mistral output to a new file as our final output for image generation prompt
        with open('image_gen_prompt.md', 'w') as final_file:
            final_file.write(response['message']['content'])

        print(response['message']['content'])
        mistral_response_printed = True  # Set the flag to True after printing the response

        print(f"Done! Generating and upscaling image with prompt. Please wait..")


# Main script
if __name__ == "__main__":
    process_file()
    # Wait for the Mistral model's response to be printed before proceeding
    while not mistral_response_printed:
        time.sleep(1)  # Wait for 1 second before checking again

    # Adjusted subprocess call to execute createimage.py without capturing output
    # This allows createimage.py to interact directly with the terminal
    try:
        subprocess.run(["python", "createimage.py"], check=True)
        print("Image created and upscaled successfully!")
        focusgen_response_printed = True  # Set the flag to True after printing the response
    except subprocess.CalledProcessError as e:
        print(f"Error executing createimage.py: {e}")

    # Use glob to find the latest image in today's date folder
    images_path = f"focusgen/{today_date}/*.png"
    list_of_images = glob.glob(images_path)
    latest_image_path = max(list_of_images, key=os.path.getctime)

    # Define the new image path using base_name
    new_image_path = f"focusgen/{today_date}/{base_name}.png"

    # Rename the original image to the new path
    try:
        os.rename(latest_image_path, new_image_path)
        print(f"Image renamed to {base_name}.png successfully.")
    except OSError as e:
        print(f"Error renaming image: {e}")
    
    while not focusgen_response_printed:
        time.sleep(1)
    cropandsave = subprocess.run(["python", "cropandsave.py"], check=True, capture_output=True, text=True)
    print(cropandsave.stdout)
    print("Image converted to deliverable resolution formats.")

    # Add this code snippet to run mockupgen.py after cropandsave.py completes
    mockupgen = subprocess.run(["python", "mockupgen.py"], check=True, capture_output=True, text=True)
    print(mockupgen.stdout)
    print("Mockups generated successfully.")


    # Function to create a folder and move images
    def create_folder_and_move_images(today_date):
        from random import randint
        # Generate a random 4-digit folder name
        folder_name = f"{randint(1000, 9999)}"  # Ensures a 4-digit number
        new_folder_path = os.path.join("export/", folder_name)
        os.makedirs(new_folder_path, exist_ok=True)
        
        # Define the source path where images are currently stored
        source_path = f"focusgen/{today_date}"
        # Get all image files from the source directory
        image_files = [f for f in os.listdir(source_path) if os.path.isfile(os.path.join(source_path, f))]
        
        # Move each image to the new folder
        for image_file in image_files:
            shutil.move(os.path.join(source_path, image_file), os.path.join(new_folder_path, image_file))
        
        print(f"All images moved to {new_folder_path}.")
        return new_folder_path

    # Call the function after mockupgen.py execution and store the returned path in a variable
    new_folder_path = create_folder_and_move_images(today_date)

    # Utility function to read file contents
    def read_file_contents(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    # Adjusted make_ollama_call function
    print("Using Ollama to generate Title and Tags...")
    def make_ollama_call(new_folder_path):
        # Read the contents of the files
        extracted_html_text = read_file_contents('extracted_html_text.md')
        image_gen_prompt = read_file_contents('image_gen_prompt.md')
        
        # Concatenate the contents with a newline between them
        userprompt_content = f"Here is the extracted_html_text.md file:\n{extracted_html_text}\n\nHere is the image_gen_prompt.md file:\n{image_gen_prompt}"

        
        # Ollama chat call (assuming the rest of the function setup is correct and remains unchanged)
        response = ollama.chat(
            model='mistral-openorca',
            keep_alive=0,
            messages=[
                {
                    'role': 'system',
                    'content': """ 
                    Objective: Your task is to generate a new product listing for Etsy. This involves crafting product tags and a new product title. You will work with two files:
  - The first file, named `{extracted_html_text}`, contains the title and some tags from another best-selling product in the desired category. This serves as a template for the format and category relevance of your new product.
  - The second file, named `{image_gen_prompt}`, provides a description of the new product's image.

Process Overview:
  - Extract Information: Begin by reading the content from the two specified files.
    - From `{extracted_html_text}`, note the product title's format and the pre-existing tags related to the product category. Understand that these are your templates for format and category alignment.
    - From `{image_gen_prompt}`, extract the new image description to use as the basis for your new product title and tags.

  - Tag Generation: 
    - Use the first six tags from the best-selling product as a starting point. These tags, extracted from the `{extracted_html_text}` file, anchor your new product in the desired category(do not use any tags including the original product authors name like "mitartprints" "northprints" etc).
    - Generate seven new tags based on the new image description in the `{image_gen_prompt}` file. These should be relevant to the Etsy product category and specifically tailored to the new product's features and appeal.

  - Title Creation:
    - Develop a new product title using the format of the best-selling product's title as a guide. However, tailor the title to reflect the new product's features as described in the new image description. This title should be catchy, relevant, and designed to attract Etsy shoppers.

Output Format:
  - Present the results in the following structured format:

Title: [New product title inspired by the format of the best-selling product and tailored to the new image description]

Tags: [Combine the six pre-existing tags from the best-selling product with the seven new tags you've generated, for example: Handmade, eco-friendly, custom design, digital print, unique gift, vintage-inspired, art deco, modern decor, personalized option, home styling, office accessory, collector's item, limited edition]

Guidelines:
  - Ensure the new tags encompass a variety of aspects related to the product, such as design, use, and target audience.
  - The new product title should be influenced by the best-selling product's title format but must accurately reflect the essence and uniqueness of the new product based on the new image description.
  - Creativity and insight are crucial for generating appealing tags and titles that will stand out to Etsy shoppers, increasing visibility and attractiveness of the new product.
  """,
                },
                {
                    'role': 'user',
                    'content': userprompt_content,
                },
            ]
        )
        
        # Save the response in the new folder
        final_output_path = os.path.join(new_folder_path, 'tagsandtitle.md')
        with open(final_output_path, 'w') as final_file:
            final_file.write(response['message']['content'])
        
        print(response['message']['content'])

    # Ensure 'new_folder_path' is correctly defined before calling make_ollama_call()
    make_ollama_call(new_folder_path)  # Pass the folder path as an argument
    # os remove any images inside extracted_images folder
    for image in os.listdir('extracted_images'):
        os.remove(os.path.join('extracted_images', image))

    print("Done!")
