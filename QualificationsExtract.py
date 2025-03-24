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
                    
        
    # reverse the created dictionary and write to file to make it easier to read and decide how to catagorize the qualifications   
    val_based_rev = {k: v for k, v in sorted(skills_dict.items(), key=lambda item: item[1], reverse=True)}
    f = open("demofile2.txt", "a")
    for key, value in val_based_rev.items():
        f.write(f"{key}: {value}\n")
    f.close()
    #open and read the file after the appending:
    f = open("demofile2.txt", "r")
    print(f.read())

                
    

search_quals(df['Qualifications'])