import ollama
from PIL import ImageGrab
import tempfile
import os


## this code has nothing to do with autoetsy but its an interesting quick way to test llava.
## It will simply look at whatever image is currently copied to your clipboard.

# Initialize an empty dictionary to store responses
outputs = {}

# Assuming 'i' is part of a loop not shown here
# For demonstration, 'i' is set to 1
i = 1

# Grab the image from the clipboard
clipboard_image = ImageGrab.grabclipboard()

# Use a temporary file to save the clipboard image
with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmpfile:
    clipboard_image.save(tmpfile, format="JPEG")
    image_file_name = tmpfile.name  # This will be used in the ollama call

response = ollama.chat(
    model='llava',
    keep_alive=0,
    messages=[
        {
            'role': 'user',
            'content': """What do you see in this image?""",
            'images': [image_file_name],  # Use the image file saved from clipboard
        },
    ]
)

outputs[f'Run {i}'] = response['message']['content']

# Print outputs to console instead of writing to a file
for key, value in outputs.items():
    print(f"{key}: {value}\n")
# Cleanup: Remove the temporary file after use
os.remove(image_file_name)
