import sys
import ollama

# Retrieve the image file name from the command line arguments
image_file_name = 'pull_1951.jpg'

response = ollama.chat(
    model='llava',
    messages=[
        {
            'role': 'user',
            'temperature': 0,
            'content': """explain the painting only""",
            'images': [image_file_name],  # Use the dynamically passed image file name
        },
    ]
)

print(response['message']['content'])
