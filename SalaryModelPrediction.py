import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Load the processed data
data = pd.read_csv('cleaned_job_listings.csv')

# Apply one-hot encoding to the 'Standardized Job Title' column
one_hot_encoded_titles = pd.get_dummies(data['Standardized Job Title'], prefix='JobTitle')

# Concatenate the one-hot encoded columns with the original dataset
data = pd.concat([data, one_hot_encoded_titles], axis=1)

# Ensure the 'Salary' column exists and drop rows with missing values
if 'Salary' in data.columns:
    data = data.dropna(subset=['Salary'])
else:
    raise ValueError("The 'Salary' column is missing from the dataset.")

# Define features (X) and target (y) AFTER dropping rows with missing values
X = data[one_hot_encoded_titles.columns]  # Use the one-hot encoded columns from the updated dataset
y = data['Salary']                        # Target variable (salaries)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest Regressor
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Make predictions on the test set
y_pred_rf = rf_model.predict(X_test)

# Evaluate the model
mse_rf = mean_squared_error(y_test, y_pred_rf)
r2_rf = r2_score(y_test, y_pred_rf)

print(f"Random Forest - Mean Squared Error: {mse_rf}")
print(f"Random Forest - R-squared: {r2_rf}")

# Feature importance
feature_importances = pd.DataFrame({
    'Job Title': X.columns,
    'Importance': rf_model.feature_importances_
}).sort_values(by='Importance', ascending=False)

print(feature_importances)

# Plot the feature importances as a bar graph
plt.figure(figsize=(10, 6))
plt.barh(feature_importances['Job Title'], feature_importances['Importance'], color='lightgreen')
plt.title('Job Title Importance in Random Forest Model')
plt.xlabel('Importance')
plt.ylabel('Job Title')
plt.gca().invert_yaxis()  # Invert y-axis to show the most important job title at the top
plt.tight_layout()
plt.show()