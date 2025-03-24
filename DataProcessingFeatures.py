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

# Mapping function for standardizing job titles
def standardize_job_title(title):
    title_lower = title.lower()
    if 'data scientist' in title_lower:
        return 'Data Scientist'
    elif 'data analyst' in title_lower or 'business analyst' in title_lower:
        return 'Data Analyst'
    elif 'ai' in title_lower or 'ml' in title_lower or 'artificial intelligence' in title_lower:
        return 'AI Engineer'
    elif 'engineer' in title_lower or 'developer' in title_lower:
        if 'frontend' in title_lower or 'front end' in title_lower or 'front-end' in title_lower:
            return 'Frontend Developer'
        elif 'backend' in title_lower or 'back-end' in title_lower or 'back end' in title_lower:
            return 'Backend Developer'
        elif 'full stack' in title_lower or 'full-stack' in title_lower:
            return 'Full Stack Developer'
        elif 'software' in title_lower:
            return 'Software Engineer'
        elif 'engineer' in title_lower:
            return 'Engineer'
        else:
            return 'Developer'
    elif 'devops' in title_lower:
        return 'DevOps Engineer'
    elif 'cloud' in title_lower:
        return 'Cloud Engineer'
    elif 'project manager' in title_lower:
        return 'Project Manager'
    elif 'manager' in title_lower:
        return 'Product Manager'
    elif 'cybersecurity' in title_lower or 'security' in title_lower:
        return 'Cybersecurity Specialist'
    elif 'analyst' in title_lower:
        return 'Analyst'
    else:
        return 'Other'

# Apply the function to standardize job titles
df['Standardized Job Title'] = df['Job Title'].apply(standardize_job_title)

# Display the first few rows with the new column
# print(df[['Job Title', 'Standardized Job Title']])


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

# function to keep the lower end of salaries
def standardized_salaries(salary):
    # Use regex to extract the first number
    match = re.search(r'\d+', str(salary))
    return match.group() if match else salary

df["Salary"] = df["Salary"].apply(clean_salary)
df["Salary"] = df["Salary"].apply(standardized_salaries)

# Convert Qualifications from string to list
def parse_qualifications(qualifications):
    try:
        return ast.literal_eval(qualifications) if isinstance(qualifications, str) else ["N/A"]
    except (ValueError, SyntaxError):
        return ["N/A"]



df["Qualifications"] = df["Qualifications"].apply(parse_qualifications)

# Reorder columns
df = df[["Standardized Job Title", "Salary", "Company Name", "Qualifications", "Job Title",  "Company Location"]]

# Save cleaned data to a new CSV file
cleaned_file_path = "cleaned_job_listings.csv"
df.to_csv(cleaned_file_path, index=False, quoting=1)  # quoting=1 ensures text fields are properly quoted
print(f"Cleaned data saved to {cleaned_file_path}")
data = read_csv("cleaned_job_listings.csv")
#salaries = data['Salary'].tolist()
#print(salaries)