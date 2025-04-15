import pandas as pd
from pandas import *
import ast
import math  # Import math for rounding up
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.preprocessing import LabelEncoder
pd.set_option('display.max_columns', None)  # Show all columns in the DataFrame

# Load the CSV file
file_path = "cleaned_job_listings.csv"
data = pd.read_csv(file_path)

# preprocessing function to clean the data for model training
# job titles will most likely use label encoding or one hot encoding
def preprocess_inputs(df):
    df = df.copy()

    #Drop Job Title column, Company Location column, and Company Name column
    df.drop(columns=["Job Title", "Company Location", "Company Name"], inplace=True)

    # Fill missing or empty values in the Salary column with the mean
    df["Salary"] = pd.to_numeric(df["Salary"], errors="coerce")  # Ensure Salary is numeric
    mean_salary = df["Salary"].mean()  # Calculate the mean
    rounded_mean_salary = math.ceil(mean_salary)  # Round up the mean
    df["Salary"].fillna(rounded_mean_salary, inplace=True)  # Fill NaN with rounded-up mean

    # Split Qualification Type Frequency into separate columns
    qualification_freq = df["Qualification Type Frequency"].apply(ast.literal_eval)
    df["prog_lang_freq"] = qualification_freq.apply(lambda x: x[0])
    df["exp_freq"] = qualification_freq.apply(lambda x: x[1])
    df["comp_freq"] = qualification_freq.apply(lambda x: x[2])
    df["oth_freq"] = qualification_freq.apply(lambda x: x[3])

    # test if the qualification frequency columns are created correctly using multi label binarizer
    mlb = MultiLabelBinarizer()
    qualifications = df["Qualifications"].apply(ast.literal_eval)  # Convert string to list
    qualifications_encoded = mlb.fit_transform(qualifications)
    qualifications_df = pd.DataFrame(qualifications_encoded, columns=mlb.classes_, index=df.index)
    df = pd.concat([df, qualifications_df], axis=1)
    df.drop(columns=["Qualifications"], inplace=True)

    # apply label encoding to  the standardized job title column
    label_encoder = LabelEncoder()
    df["Standardized Job Title"] = label_encoder.fit_transform(df["Standardized Job Title"])

    # Drop the original Qualification Type Frequency column
    df.drop(columns=["Qualification Type Frequency"], inplace=True)

    return df

X = preprocess_inputs(data)
# print(X.head())
#print(X.select_dtypes(include=['object']).columns)  # Check for object columns
#print(X['Qualifications'].unique()) these features are nominal
#print(X['qualifications'].value_counts())  # Check for unique values in the Qualifications column

# Write the processed data to a new CSV file
output_file_path = "encoded_job_listings.csv"
X.to_csv(output_file_path, index=False)

print(f"Processed data has been written to {output_file_path}")