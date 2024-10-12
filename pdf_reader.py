from PyPDF2 import PdfReader
from summarizer import summarize_reviews
import json

def extract_text_from_pdf(pdf_path):
    json_file = {}
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        lines = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                lines.extend(page_text.split('\n'))
        for i, line in enumerate(lines):  # Use enumerate to get both index and line
            if line == "1. Provide an overall rating of the instruction.":
                json_file["Q1"] = float(lines[i+4].split()[-1])
            elif line == "2. Provide an overall rating of the course.":
                json_file["Q2"] = float(lines[i+4].split()[-1])
            elif line == "3. Estimate how much you learned in the course.":
                json_file["Q3"] = float(lines[i+4].split()[-1])
            elif line == "4. Rate the effectiveness of the course in challenging you intellectually.":
                json_file["Q4"] = float(lines[i+4].split()[-1])
            elif line == "5. Rate the effectiveness of the instructor in stimulating your interest in the subject.":
                json_file["Q5"] = float(lines[i+4].split()[-1])
            elif line == "6. Estimate the average number of hours per week you spent on this course outside of class and lab time.":
                mode_hours_spent = ""
                local_max = 0.0
                for j in range(3, 9):
                    percentage = float(lines[i+j].split()[-1].replace('%', ''))
                    if percentage > local_max:
                        local_max = percentage
                        mode_hours_spent = " ".join(lines[i+j].split()[0:2])
                json_file["Q6"] = mode_hours_spent
            elif line == "ESSAY QUESTIONS":
                comments = ""
                j = i + 3
                while j < len(lines) and lines[j] != "DEMOGRAPHICS":
                    comments += lines[j]
                    j += 1
                json_file["comments"] = summarize_reviews(comments, 1500)
    return json.dumps(json_file)

# Example usage
pdf_text = extract_text_from_pdf('connor_bain.pdf')

with open('extracted_data.json', 'w') as json_file:
    json.dump(json.loads(pdf_text), json_file, indent=4)  # Write the JSON data with indentation for readability

print(pdf_text)