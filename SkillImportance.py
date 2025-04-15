import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# Load the dataset
file_path = "encoded_job_listings.csv"
data = pd.read_csv(file_path)

# Define features (skills) and target (e.g., Salary or Job Role)
skills_columns = ["prog_lang_freq", "exp_freq", "comp_freq", "oth_freq"]  # Replace with actual skill-related columns
target_column = "Salary"  # Replace with the target column (e.g., Job Role or Salary)

X = data[skills_columns]
y = data[target_column]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)

# Train a Random Forest model
rf_model = RandomForestRegressor(random_state=1)
rf_model.fit(X_train, y_train)

# Get feature importances
feature_importances = rf_model.feature_importances_

# Create a DataFrame for visualization
importance_df = pd.DataFrame({
    "Skill": skills_columns,
    "Importance": feature_importances
}).sort_values(by="Importance", ascending=False)

# Plot feature importances
plt.figure(figsize=(10, 6))
plt.barh(importance_df["Skill"], importance_df["Importance"], color="skyblue")
plt.xlabel("Importance")
plt.ylabel("Skill")
plt.title("Feature Importance of Skills")
plt.gca().invert_yaxis()  # Invert y-axis for better readability
plt.show()

# Print the sorted feature importance
print(importance_df)