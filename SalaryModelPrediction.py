import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import mean_squared_error, r2_score

# Load the processed data
data = pd.read_csv('cleaned_job_listings.csv')

# Convert 'Qualification Type Frequency' column from strings to lists
data['Qualification Type Frequency'] = data['Qualification Type Frequency'].apply(eval)

# Calculate the total number of qualifications for each row
data['Total Qualifications'] = data['Qualification Type Frequency'].apply(sum)

# Extract individual qualification types as separate columns
qualification_types = ["Prog Lang", "Exp", "CmpSc Skills", "Other"]
for i, label in enumerate(qualification_types):
    data[label] = data['Qualification Type Frequency'].apply(lambda x: x[i])

# Ensure the 'Salary' column exists and drop rows with missing values
if 'Salary' in data.columns:
    data = data.dropna(subset=['Salary'])
else:
    raise ValueError("The 'Salary' column is missing from the dataset.")

# Remove extreme salary outliers
salary_threshold = data['Salary'].quantile(0.99)  # Set threshold as the 99th percentile
data = data[data['Salary'] <= salary_threshold]

# Define features (X) and target (y)
X = data[['Total Qualifications'] + qualification_types]  # Use total qualifications and types as features
y = data['Salary']  # Target variable (salaries)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Linear Regression model
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)

# Make predictions on the test set
y_pred_lr = lr_model.predict(X_test)

# Evaluate the model
mse_lr = mean_squared_error(y_test, y_pred_lr)
r2_lr = r2_score(y_test, y_pred_lr)

print(f"Linear Regression - Mean Squared Error: {mse_lr}")
print(f"Linear Regression - R-squared: {r2_lr}")

# Plot the total qualifications vs. salary, color-coded by job titles
plt.figure(figsize=(10, 6))
sns.scatterplot(
    x=data['Total Qualifications'],
    y=data['Salary'],
    hue=data['Standardized Job Title'],  # Color-coded by job titles
    palette='tab10',  # Use a more distinguishable color palette
    alpha=0.7
)
plt.title('Total Qualifications vs. Salary (Color-Coded by Job Title)')
plt.xlabel('Total Qualifications')
plt.ylabel('Salary')
plt.legend(title='Job Title', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()