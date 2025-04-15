import pandas as pd
from pandas import *
import ast
import re
import sklearn
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np


file_path = "encoded_job_listings.csv"
data = pd.read_csv(file_path)

def model(df):
    # split df into X and y (x will only care about job titles for this test)
    # Drop the specified columns
    columns_to_drop = [
        "Standardized Job Title",
        "Salary",
        "prog_lang_freq",
        "exp_freq",
        "comp_freq",
        "oth_freq"
    ]
    X = df.drop(columns=columns_to_drop)
    y = df["Salary"]

    # train test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.7, shuffle=True, random_state=1)
    return X_train, X_test, y_train, y_test

# X, y = model(data)
# print(X.head())
# print(y.head())

X_train, X_test, y_train, y_test = model(data)
# print(X_train.head())
# print(X_test.head())
# print(y_train.head())
# print(y_test.head())


from sklearn.linear_model import LinearRegression
# 0.017
lin_reg = LinearRegression()
lin_reg.fit(X_train, y_train)
lin_r2 = lin_reg.score(X_test, y_test)
print("Linear Regression R2 Score:", lin_r2)

from xgboost import XGBRegressor
# 0.9985573627848441
xgb_model = XGBRegressor()
xgb_model.fit(X_train, y_train)
xgb_r2 = xgb_model.score(X_test, y_test)
print("XGBoost R2 Score:", xgb_r2)

from sklearn.ensemble import RandomForestRegressor
# 0.8222055911289595
rf_model = RandomForestRegressor(random_state=1)
rf_model.fit(X_train, y_train)
rf_r2 = rf_model.score(X_test, y_test)
print("Random Forest R2 Score:", rf_r2)


# Predictions for Linear Regression
lin_reg_predictions = lin_reg.predict(X_test)

# Predictions for XGBoost
xgb_predictions = xgb_model.predict(X_test)

# Predictions for Random Forest
rf_predictions = rf_model.predict(X_test)

# Define a threshold for outlier removal (e.g., 1.5 times the interquartile range)
def remove_outliers(y_actual, y_pred):
    q1 = np.percentile(y_actual, 25)  # First quartile
    q3 = np.percentile(y_actual, 75)  # Third quartile
    iqr = q3 - q1  # Interquartile range
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    # Filter data to remove outliers
    mask = (y_actual >= lower_bound) & (y_actual <= upper_bound)
    return y_actual[mask], y_pred[mask]

# Remove outliers for each model
y_test_filtered, lin_reg_predictions_filtered = remove_outliers(y_test, lin_reg_predictions)
_, xgb_predictions_filtered = remove_outliers(y_test, xgb_predictions)
_, rf_predictions_filtered = remove_outliers(y_test, rf_predictions)

# Plotting the results
plt.figure(figsize=(18, 6))

# Linear Regression Visualization
plt.subplot(1, 3, 1)
plt.scatter(y_test_filtered, y_test_filtered, alpha=0.6, color='blue', label='Actual')  # Actual values in blue
plt.scatter(y_test_filtered, lin_reg_predictions_filtered, alpha=0.6, color='red', label='Predicted')  # Predicted values in red
plt.plot([y_test_filtered.min(), y_test_filtered.max()], [y_test_filtered.min(), y_test_filtered.max()], 'k--', lw=2)
plt.title("Linear Regression: Actual vs Predicted (Outliers Removed)")
plt.xlabel("Actual Salary")
plt.ylabel("Predicted Salary")
plt.legend()

# XGBoost Visualization
plt.subplot(1, 3, 2)
plt.scatter(y_test_filtered, y_test_filtered, alpha=0.6, color='blue', label='Actual')  # Actual values in blue
plt.scatter(y_test_filtered, xgb_predictions_filtered, alpha=0.6, color='red', label='Predicted')  # Predicted values in red
plt.plot([y_test_filtered.min(), y_test_filtered.max()], [y_test_filtered.min(), y_test_filtered.max()], 'k--', lw=2)
plt.title("XGBoost: Actual vs Predicted (Outliers Removed)")
plt.xlabel("Actual Salary")
plt.ylabel("Predicted Salary")
plt.legend()

# Random Forest Visualization
plt.subplot(1, 3, 3)
plt.scatter(y_test_filtered, y_test_filtered, alpha=0.6, color='blue', label='Actual')  # Actual values in blue
plt.scatter(y_test_filtered, rf_predictions_filtered, alpha=0.6, color='red', label='Predicted')  # Predicted values in red
plt.plot([y_test_filtered.min(), y_test_filtered.max()], [y_test_filtered.min(), y_test_filtered.max()], 'k--', lw=2)
plt.title("Random Forest: Actual vs Predicted (Outliers Removed)")
plt.xlabel("Actual Salary")
plt.ylabel("Predicted Salary")
plt.legend()

plt.tight_layout()
plt.show()
