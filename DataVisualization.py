
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import joblib

# Load the processed data
data = pd.read_csv('cleaned_job_listings.csv')

# Display the first few rows of the dataset
print(data.head())

'''
Turn the skills and qualifications into numerical data based on the catagories. This should probably be done in DataProcessingFeatures.py
Then apply those into graphs to visualise the data better. Data Training will come later.
'''