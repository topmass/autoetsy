import sys
import ollama

# Retrieve the image file name from the command line arguments
image_file_name = sys.argv[1]  # The first argument is the script name, so we use the second one.

response = ollama.chat(
    model='llava',
    messages=[
        {
            'role': 'user',
            'content': """Describe this image so that it can be used by an ai to generate a new painting, you will always only respond starting with a description like "a painting of..." you will never describe the frame or elements of the image itself only the artwork inside. """,
            'images': [image_file_name],  # Use the dynamically passed image file name
        },
    ]
)

print(response['message']['content'])
