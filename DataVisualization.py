import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the processed data
data = pd.read_csv('cleaned_job_listings.csv')

# Convert 'Qualification Type Frequency' column from strings to lists
data['Qualification Type Frequency'] = data['Qualification Type Frequency'].apply(eval)

# Calculate the sum of each index across all lists in 'Qualification Type Frequency'
index_sums = [0, 0, 0, 0]  # Assuming each list has exactly 4 numbers
for row in data['Qualification Type Frequency']:
    for i in range(len(row)):
        index_sums[i] += row[i]

# Define custom labels for the qualification types
custom_labels = ["Prog Lang", "Exp", "CmpSc Skills", "Other"]

# Plot the frequency of each qualification type
plt.figure(figsize=(8, 6))
sns.barplot(x=custom_labels, y=index_sums)
plt.title("Frequency of Each Qualification Type")
plt.xlabel("Qualification Type")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()

# Count the frequency of each job title
job_title_counts = data['Standardized Job Title'].value_counts()

# Plot the frequency of each job title
plt.figure(figsize=(10, 6))
sns.barplot(x=job_title_counts.index, y=job_title_counts.values)
plt.title("Frequency of Each Job Title")
plt.xlabel("Job Title")
plt.ylabel("Frequency")
plt.xticks(rotation=45, ha="right")  # Rotate x-axis labels for better readability
plt.tight_layout()  # Adjust layout to prevent label overlap
plt.show()
