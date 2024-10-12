from groq import Groq
import os
import json

# Load the JSON data from the extracted_data.json file
with open('extracted_data.json', 'r') as json_file:
    extracted_data = json.load(json_file)

# Initialize the Groq client
api_key = os.environ.get("GROQ_API_KEY")
if api_key is None:
    raise ValueError("GROQ_API_KEY environment variable is not set.")

client = Groq(api_key=api_key)


def summarize_reviews(reviews, max_length):
    reviews  = reviews[:max_length]
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "user",
                "content": "I am creating a tool that summarizes the reviews that students are giving to a course an its professor." +
                    "In a short 7-10 sentence paragraph, generalize these reivews to show true student sentiment, only return the paragraph" + reviews
            }
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    summary = ""
    for chunk in completion:
        summary += chunk.choices[0].delta.content or ""
    
    return summary
