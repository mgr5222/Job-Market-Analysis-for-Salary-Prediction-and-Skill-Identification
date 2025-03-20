import pandas as pd
from pandas import *
import ast
import re

# Load the CSV file
file_path = "job_listings.csv"
df = pd.read_csv(file_path)

# Handle missing values
df.fillna("N/A", inplace=True)

# Split Location into Company Name and Company Location
def split_location(location):
    if not isinstance(location, str) or not location.strip():
        return "N/A", "N/A"
    
    parts = location.split("\n")  # Split by new lines first
    if len(parts) == 2:
        return parts[0].strip(), parts[1].strip()
    
    # Improved regex to remove ratings (handles different spacing variations)
    parts = re.split(r"\s*-\s*\d+\.\d+\s*", location)  
    if len(parts) == 2:
        return parts[0].strip(), parts[1].strip()
    elif len(parts) == 1:
        return parts[0].strip(), "N/A"
    return "N/A", "N/A"

df[["Company Name", "Company Location"]] = df["Location"].apply(lambda x: pd.Series(split_location(str(x))))
df.drop(columns=["Location"], inplace=True)

# Standardize Job Titles (Example: Map variations to common names)
job_title_mapping = {
    "Software Developer": "Software Engineer",
    "Front-End Developer": "Frontend Engineer",
    "Backend Engineer": "Backend Engineer",
    "Senior Python/C++ Developer": "Senior Software Engineer",
}
df["Job Title"] = df["Job Title"].replace(job_title_mapping, regex=True)

# Convert Qualifications from string to list
def parse_qualifications(qualifications):
    try:
        return ast.literal_eval(qualifications) if isinstance(qualifications, str) else ["N/A"]
    except (ValueError, SyntaxError):
        return ["N/A"]

df["Qualifications"] = df["Qualifications"].apply(parse_qualifications)

# Convert salary to yearly average
def clean_salary(salary):
    # Remove non-numeric, non-dollar, and non-space characters
    salary = re.sub(r"[^0-9\-\$K ]", "", salary).strip()
    
    
    
    if not salary:
        return "N/A"
    
        # Handle 'K' by appending three zeros to the number
    if 'K' in salary:
        salary = re.sub(r"(\d+)K", lambda m: str(int(m.group(1)) * 1000), salary)
    
    
    # Extract all numbers after the first one until a whitespace
    numbers = re.findall(r"\d+", salary)
    if not numbers:
        return "N/A"
    
    # If the first number has fewer than 3 digits, assume it's an hourly rate
    if len(numbers[0]) < 3:
        hourly_rate = float(numbers[0])
        return f"{hourly_rate * 40 * 52:.0f}"  # Convert to yearly salary
    
    # Otherwise, return the extracted numbers as a single string
    return " ".join(numbers)


df["Salary"] = df["Salary"].apply(clean_salary)

# Reorder columns
df = df[["Job Title", "Company Name", "Company Location", "Qualifications", "Salary"]]

# Save cleaned data to a new CSV file
cleaned_file_path = "cleaned_job_listings4.csv"
df.to_csv(cleaned_file_path, index=False, quoting=1)  # quoting=1 ensures text fields are properly quoted
print(f"Cleaned data saved to {cleaned_file_path}")
data = read_csv("cleaned_job_listings4.csv")
salaries = data['Salary'].tolist()
print(salaries)