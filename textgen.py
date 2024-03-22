import requests

# Step 1: Read the content of the files
with open('extracted_html_text.md', 'r') as file:
    html_content = file.read()

with open('image_gen_prompt.md', 'r') as file:
    image_description = file.read()

# Step 2: Craft the prompt
prompt_text = f"Read the following HTML content and extract the style of the title and the tags: \n{html_content}\n Then, based on the description of a new image: \n{image_description}\n, generate a new title that mimics the style of the original title and create new tags. Use half of the original tags and generate half new tags relevant to the new image description."

# Step 3: Send the prompt to Olama using the structure from the working example
response = requests.post(
    'http://localhost:11434/api/chat',
    json={
        "model": "stablelm2",
        "messages": [
            {
                "role": "user",
                "content": prompt_text,
            },
            {
                "role": "system",
                "content": "Generate a new title and tags based on the instructions.",
            },
        ],
        "stream": False
    }
)

# Assuming the response structure is similar to the working example provided
if response.status_code == 200:
    response_data = response.json()
    try:
        # Extract the generated content from the response
        generated_content = response_data['message']['content']
        print("Generated Title and Tags:", generated_content)
        
        # Optionally, save the generated content to a file
        with open('generated_title_and_tags.md', 'w') as file:
            file.write(generated_content)
    except KeyError:
        print("KeyError: The expected key is not present in the response.")
else:
    print(f"Request failed with status code: {response.status_code}")
    print("Response content:", response.text)
