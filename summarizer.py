import os
import json  # Import the json module
from groq import Groq

# Load the JSON data from the extracted_data.json file
with open('extracted_data.json', 'r') as json_file:
    extracted_data = json.load(json_file)  # Load the JSON data into a Python dictionary

# Initialize the Groq client
api_key = os.environ.get("GROQ_API_KEY")
if api_key is None:
    raise ValueError("GROQ_API_KEY environment variable is not set.")

client = Groq(api_key=api_key)

# Truncate the comments to a maximum length
max_length = 1000
comments = extracted_data['comments'][:max_length]

# Example usage of the extracted data
completion = client.chat.completions.create(
    model="llama3-8b-8192",
    messages=[
        {
            "role": "user",
            "content": "In a short 5-6 sentence paragraph, summarize this big block of text: " + comments
        }
    ],
    temperature=1,
    max_tokens=1024,
    top_p=1,
    stream=True,
    stop=None,
)

for chunk in completion:
    print(chunk.choices[0].delta.content or "", end="")
