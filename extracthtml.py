from bs4 import BeautifulSoup
import re
import json
import os
import glob
import requests  # Import requests to download images
import base64
from urllib.parse import urlparse

# Define the path to the dump folder and pattern for files
dump_folder_path = './dump'
file_pattern = os.path.join(dump_folder_path, 'pull_*.html')
images_folder_path = './extracted_images'  # Define the path for saving images

# Ensure the images folder exists
if not os.path.exists(images_folder_path):
    os.makedirs(images_folder_path)

# Find all .html files in the dump folder that start with pull_
for file_path in glob.glob(file_pattern):
    output_content = []  # Initialize a list to collect output strings for each file
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Use BeautifulSoup to parse HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract the product/listing title
    product_title = soup.find('h1') or soup.find(class_='product-title')
    output_content.append("Product/Listing Title: " + (product_title.get_text(strip=True) if product_title else "Not Found"))

    # Extract the explore related searches category titles
    related_searches_urls = soup.find_all('a', href=True)
    related_searches_titles = []
    for url in related_searches_urls:
        match = re.search(r"market/([a-zA-Z_]+)", url['href'])
        if match:
            title = match.group(1).replace('_', ' ').title()
            related_searches_titles.append(title)

    # Deduplicate and limit to 13 titles
    related_searches_titles = list(dict.fromkeys(related_searches_titles))[:13]

    related_searches_output = ["Explore Related Searches Category Titles:"] + ["- " + title for title in related_searches_titles]
    output_content.extend(related_searches_output)

    # Find and download the first image, skipping .avif files
    first_image = soup.find('img')
    if first_image:
        image_url = first_image.get('src')
        # Skip if the image is in AVIF format
        if image_url and not image_url.startswith('data:image/avif'):
            if image_url.startswith('data:image'):
                # Process base64 encoded images that are not AVIF
                header, encoded = image_url.split(",", 1)
                image_data = base64.b64decode(encoded)
                image_format = header.split(';')[0].split('/')[1]
                # Ensure we're not dealing with AVIF format after decoding
                if image_format.lower() != 'avif':
                    image_name = os.path.basename(file_path).replace('.html', f'.{image_format}')  # Adjust the file extension based on the image format
                    image_path = os.path.join(images_folder_path, image_name)
                    with open(image_path, 'wb') as image_file:
                        image_file.write(image_data)
            else:
                # Handle regular HTTP URL images as before, excluding AVIF format
                image_response = requests.get(image_url)
                if image_response.status_code == 200:
                    image_name = os.path.basename(file_path).replace('.html', '.jpg')  # Use the same base name as the HTML file, assuming non-AVIF
                    image_path = os.path.join(images_folder_path, image_name)
                    with open(image_path, 'wb') as image_file:
                        image_file.write(image_response.content)

    # Find and download the specified image using the correct attribute
    specified_image = soup.find('img', class_='wt-max-width-full wt-horizontal-center wt-vertical-center carousel-image wt-rounded')
    if specified_image and specified_image.get('data-src-zoom-image'):
        image_url = specified_image['data-src-zoom-image']
        image_response = requests.get(image_url)
        if image_response.status_code == 200:
            image_name = os.path.basename(file_path).replace('.html', '.jpg')  # Naming the file with a unique identifier
            image_path = os.path.join(images_folder_path, image_name)
            with open(image_path, 'wb') as image_file:
                image_file.write(image_response.content)

    # Extract the number from the original HTML file's name
    file_number = re.search(r'pull_(\d+).html', file_path).group(1)

    # Construct the markdown file's name using the extracted number
    markdown_file_name = f'extracted_{file_number}.md'

    # Write the collected output to the corresponding markdown file
    with open(markdown_file_name, 'w', encoding='utf-8') as md_file:
        md_file.write('\n'.join(output_content))
