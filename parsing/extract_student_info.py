import re

def extract_student_info(clean_text: str) -> dict:
    name = "Unknown"
    rollno = "Unknown"
    
    # Search for name patterns
    name_match = re.search(r'(?i)(name|student name)[:\s]*([A-Za-z\s]+)', clean_text)
    if name_match:
        name = name_match.group(2).strip()
    
    # Search for rollno patterns
    roll_match = re.search(r'(?i)(roll|rollno|roll number|id)[:\s]*([A-Za-z0-9]+)', clean_text)
    if roll_match:
        rollno = roll_match.group(2).strip()
    
    return {"name": name, "rollno": rollno}