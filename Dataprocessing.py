import pandas as pd
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
    salary = str(salary).split("\n")[-1]  # Take last part (Removes job type if present)
    salary = re.sub(r"[^0-9\-\$ ]", "", salary).strip()  # Keep only salary range
    
    if not salary:
        return "N/A"
    
    # Convert hourly rate to yearly salary (assuming 40 hours/week, 52 weeks/year)
    hourly_match = re.search(r"\$(\d+(?:,\d+)?) per hour", salary)
    if hourly_match:
        hourly_rate = float(hourly_match.group(1).replace(",", ""))
        return f"{hourly_rate * 40 * 52:.2f}"
    
    # Convert salary range to average
    range_match = re.findall(r"\$(\d+(?:,\d+)?)", salary)
    if len(range_match) == 2:
        low = float(range_match[0].replace(",", ""))
        high = float(range_match[1].replace(",", ""))
        return f"{(low + high) / 2:.2f}"
    
    # Convert single annual salary value
    single_match = re.search(r"\$(\d+(?:,\d+)?)", salary)
    if single_match:
        return single_match.group(1).replace(",", "")
    
    return "N/A"

df["Salary"] = df["Salary"].apply(clean_salary)

# Reorder columns
df = df[["Job Title", "Company Name", "Company Location", "Qualifications", "Salary"]]

# Save cleaned data to a new CSV file
cleaned_file_path = "cleaned_job_listings.csv"
df.to_csv(cleaned_file_path, index=False, quoting=1)  # quoting=1 ensures text fields are properly quoted

print(f"Cleaned data saved to {cleaned_file_path}")
