from PyPDF2 import PdfReader
import json
import re

# Load the PDF
pdf_path = "/mnt/data/WorldsWithoutNumber_FreePDF_Lightweight_040221.pdf"
reader = PdfReader(pdf_path)

# Extract text from page 10 (index 9)
page = reader.pages[9]
text = page.extract_text()

# Extract skills from the page by identifying the pattern of skills and descriptions
# We'll assume each skill is followed by a colon or a dash and a description
# Start by extracting potential skill lines from the text
lines = text.split('\n')

# Initialize the skills dictionary
skills_dict = {}
current_skill = ""

# Parse lines into skill dictionary
for line in lines:
    if re.match(r"^[A-Z][a-z]+:", line):  # Skill line (e.g., "Connect:")
        skill, description = line.split(":", 1)
        current_skill = skill.strip()
        skills_dict[current_skill] = description.strip()
    elif current_skill:
        # Append to the current skill's description if it's a continuation
        skills_dict[current_skill] += " " + line.strip()

# Save to JSON
output_path = "/mnt/data/wwn_skills.json"
with open(output_path, "w") as f:
    json.dump(skills_dict, f, indent=2)

output_path
