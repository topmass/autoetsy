import os
from datetime import datetime
from PIL import Image, ImageChops

# Generate the directory path for today's date
todays_date = datetime.now().strftime("%Y-%m-%d")
directory_path = f"focusgen/{todays_date}"

def composite_image_with_mockup(input_image_path, mockupfill_path, mockup_path, output_path):
    # Load the input image
    try:
        input_image = Image.open(input_image_path)
    except FileNotFoundError:
        print(f"Input image {input_image_path} not found.")
        return

    # Load the mockupfill image
    try:
        mockupfill = Image.open(mockupfill_path)
    except FileNotFoundError:
        print(f"Mockup fill image {mockupfill_path} not found.")
        return
    
    # Find the white rectangle by comparing mockupfill to a fully transparent image
    transparent_image = Image.new('RGBA', mockupfill.size, (0, 0, 0, 0))
    diff = ImageChops.difference(mockupfill.convert('RGBA'), transparent_image)
    bbox = diff.getbbox()
    
    if bbox:
        # Resize the input image to fit the white rectangle
        input_image_resized = input_image.resize((bbox[2] - bbox[0], bbox[3] - bbox[1]))
        
        # Paste the resized input image onto mockupfill.png without using it as a mask
        mockupfill.paste(input_image_resized, bbox[:2])
    
    # Load the mockup.png
    try:
        mockup = Image.open(mockup_path)
    except FileNotFoundError:
        print(f"Mockup image {mockup_path} not found.")
        return
    
    # Ensure both images are in 'RGBA' to support transparency in compositing
    mockupfill_converted = mockupfill.convert('RGBA')
    mockup_converted = mockup.convert('RGBA')

    # Composite mockup.png on top of the modified mockupfill.png
    final_image = Image.alpha_composite(mockupfill_converted, mockup_converted)
    
    # Save the final composite image
    final_image.save(output_path, 'PNG')
    print(f"Composite image created and saved as {output_path}.")

def composite_image_with_mockup_closeup(input_image_path, mockupfill_path, mockup_path, output_path):
    # Load the input image
    try:
        input_image = Image.open(input_image_path)
    except FileNotFoundError:
        print(f"Input image {input_image_path} not found.")
        return

    # Load the mockupfill image
    try:
        mockupfill = Image.open(mockupfill_path)
    except FileNotFoundError:
        print(f"Mockup fill image {mockupfill_path} not found.")
        return

    # Paste the input image onto mockupfill.png aligning the bottom-left corner
    mockupfill.paste(input_image, (0, mockupfill.height - input_image.height))

    # Load the mockup.png
    try:
        mockup = Image.open(mockup_path)
    except FileNotFoundError:
        print(f"Mockup image {mockup_path} not found.")
        return

    # Ensure both images are in 'RGBA' to support transparency in compositing
    mockupfill_converted = mockupfill.convert('RGBA')
    mockup_converted = mockup.convert('RGBA')

    # Composite mockup.png on top of the modified mockupfill.png
    final_image = Image.alpha_composite(mockupfill_converted, mockup_converted)

    # Save the final composite image
    final_image.save(output_path, 'PNG')
    print(f"Closeup composite image created and saved as {output_path}.")

# Assuming the root directory is 'c:/code/etsy/', as indicated by your command prompt
root_directory = 'c:/code/etsy/'

# Search for the image file
try:
    files_in_directory = os.listdir(directory_path)
    image_found = False
    for file_name in files_in_directory:
        if file_name.endswith("_5x7.jpg"):
            print(f"Found image: {file_name}")
            image_path = os.path.join(directory_path, file_name)
            # Iterate over mockup and mockup fill pairs
            for i in range(1, 5):  # For mockup1.png to mockup4.png
                mockupfill_path = os.path.join(root_directory, f'mockup{i}fill.png')
                mockup_path = os.path.join(root_directory, f'mockup{i}.png')
                output_path = os.path.join(directory_path, f'result_mockup{i}.png')
                composite_image_with_mockup(image_path, mockupfill_path, mockup_path, output_path)
            image_found = True
            # Generate the closeup mockup
            mockupfill_path = os.path.join(root_directory, 'mockup5fill.png')
            mockup_path = os.path.join(root_directory, 'mockup5.png')
            output_path = os.path.join(directory_path, 'result_mockup5.png')
            composite_image_with_mockup_closeup(image_path, mockupfill_path, mockup_path, output_path)
            break
    if not image_found:
        print("No image file ending with _5x7.jpg found in today's directory.")
except FileNotFoundError:
    print(f"The directory {directory_path} does not exist.")