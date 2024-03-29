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

def create_zoom_effect_video(input_image_path, output_video_path, duration=6, fps=24):  # Duration doubled to reduce speed
    from PIL import Image
    import imageio
    import numpy as np

    # Load and convert the input image
    input_image = Image.open(input_image_path).convert('RGBA')
    
    # Scale down the input image by a factor of 3
    scaled_width = input_image.width // 3
    scaled_height = input_image.height // 3
    scaled_image = input_image.resize((scaled_width, scaled_height))
    
    # The initial frame will be the scaled image centered and cropped to fit a 512x512 frame if necessary
    if scaled_width > 512 or scaled_height > 512:
        initial_crop = scaled_image.crop(((scaled_width - 512) // 2, (scaled_height - 512) // 2, (scaled_width + 512) // 2, (scaled_height + 512) // 2))
    else:
        initial_crop = scaled_image

    frames = []
    total_frames = duration * fps
    zoom_step = (512 - min(scaled_width, scaled_height)) / total_frames / 4  # Zoom amount reduced by 50%

    for frame in range(total_frames):
        current_size = min(scaled_width, scaled_height) + frame * zoom_step
        current_left = max(0, (scaled_width - current_size) // 2)
        current_top = max(0, (scaled_height - current_size) // 2)
        
        frame_image = scaled_image.crop((current_left, current_top, current_left + current_size, current_top + current_size))
        frame_image = frame_image.resize((512, 512))
        
        frames.append(frame_image)
    
    # Convert PIL images to numpy arrays as required by imageio
    frames = [imageio.core.util.Array(np.array(frame)) for frame in frames]

    # Save the frames as an MP4 video
    imageio.mimwrite(output_video_path, frames, fps=fps, format='mp4')
    print(f"Zoom effect video created and saved as {output_video_path}.")

# Search for the image file
try:
    files_in_directory = os.listdir(directory_path)
    image_found = False
    for file_name in files_in_directory:
        if file_name.endswith("_5x7.jpg"):
            print(f"Found image: {file_name}")
            image_path = os.path.join(directory_path, file_name)
            for i in range(1, 5):
                mockupfill_path = f'mockup{i}fill.png'
                mockup_path = f'mockup{i}.png'
                output_path = os.path.join(directory_path, f'result_mockup{i}.png')
                composite_image_with_mockup(image_path, mockupfill_path, mockup_path, output_path)
            image_found = True
            output_video_path = os.path.join(directory_path, 'result_mockup5.mp4')
            create_zoom_effect_video(image_path, output_video_path)
            break
    if not image_found:
        print("No image file ending with _5x7.jpg found in today's directory.")
except FileNotFoundError:
    print(f"The directory {directory_path} does not exist.")