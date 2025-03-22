# Extract qualifications from the cleaned_job_listings.csv and put them into a dictionary to see how many of each were found
# and to see which ones can be ignored
import pandas as pd
from pandas import *
import ast
import re

file = "cleaned_job_listings.csv"
df = pd.read_csv(file)


# Convert Qualifications from string to list
def parse_qualifications(qualifications):
    try:
        return ast.literal_eval(qualifications) if isinstance(qualifications, str) else ["N/A"]
    except (ValueError, SyntaxError):
        return ["N/A"]

# change the csv qualifications to the list
df["Qualifications"] = df["Qualifications"].apply(parse_qualifications)

def search_quals(qualifications):
    skills_dict = {}
    # print(qualifications[0][1])
    for entry in qualifications:
        if isinstance(entry, list):  # Ensure entry is a list
            for skill in entry:
                if skill not in skills_dict.keys():
                    skills_dict[skill] = 1
                else:
                    skills_dict[skill] += 1
                    
    val_based_rev = {k: v for k, v in sorted(skills_dict.items(), key=lambda item: item[1], reverse=True)}
    print(val_based_rev)
                
    

search_quals(df['Qualifications'])