import pandas as pd
import numpy as np
import sys
import os
os.chdir("G:\My Drive\courses\data visualization")
print(os.getcwd())
data = pd.read_csv('NAVCO2-1_EDITED.csv',  encoding= 'unicode_escape')
progress = {5: -1}
data['progress'] = data['progress'].replace(progress)

progress_values = {0: "status quo", 1: "visible gains short of concessions", 2: "limited concession achieved", 3: "significant concessions achieved", 4: "complete success", -1: "ends in failure", -99: "unknown"}

data['progress_names'] = data['progress'].map(progress_values)


goals_values = {0: "regime change", 1: "significant institutional reform", 2: "policy change", 3: "territorial secession", 4: "greater autonomy", 5: "greater autonomy", -99: "unknown"}
data["goals_names"] = data["camp_goals"].map(goals_values)

data = data[data['goals_names'].isin(["regime change", "greater autonomy"])]


population = pd.read_csv('population.csv')
location_map = {"Russian Federation" : "Russia"}
population["Location"] = population["Location"].replace(location_map)



population["PopTotal"] = population["PopTotal"] * 1000
# First merge using loc_iso and LocID
merged_df = pd.merge(data, population[['LocID', 'Time', 'PopTotal']], left_on=['loc_iso', 'year'], right_on=['LocID', 'Time'], how='left')



# Create a mask for rows where PopDensity is missing
missing_mask = merged_df['PopTotal'].isnull()

# Second merge using location and year for the missing rows
merged_df['temp_pop'] = pd.merge(data, population[['Location', 'Time', 'PopTotal']], left_on=['location', 'year'], right_on=['Location', 'Time'], how='left')['PopTotal']

merged_df.loc[missing_mask, 'PopTotal'] = merged_df.loc[missing_mask, 'temp_pop']

# Drop the unnecessary loc_iso and LocID columns


merged_df["percent_participation"] = (merged_df["total_part"] / merged_df["PopTotal"]) * 100

bad_values = ['64_1968', '74_1953', '75_1989', '119_1989', '120_1981', '156_1958', '156_1959', '156_1960',
                          '156_1961', '156_1962', '156_1963', '156_1964', '156_1965', '184_1962', '184_1963', '184_1964',
                          '184_1965', '184_1966', '184_1967', '184_1968', '184_1969', '240_1989', '245_1986',
                          '280_1964', '280_1965', '280_1966',  '389_1979', '389_1980',
                          '389_1981', '389_1982']

merged_df = merged_df[~ merged_df["campyearid"].isin(bad_values)]



merged_df["population_bad"] = (merged_df['PopTotal'].isnull() ) | (merged_df['total_part'] == -99)

del merged_df['loc_iso']
del merged_df['LocID']
del merged_df['temp_pop']


merged_df.rename(columns = {'goals_names':'goal_names'}, inplace = True)

repression_names = {0: "none", 1: "mild repression", 2: "moderate repression", 3: "extreme repression", -99: "unknown"}

merged_df["repression_names"] = merged_df["repression"].map(repression_names)

merged_df.sort_values(by='id', ascending=False)

# Initialize an empty list to store modified violence labels

id_to_violence = {}
# Iterate over each group
for id in merged_df.id.unique():

    campaign = merged_df[merged_df.id == id]
    if len(campaign.prim_meth.unique()) == 2:
        id_to_violence[id] = "sometimes violent"

    elif int(list(campaign.prim_meth.unique())[0]) == 0:
        id_to_violence[id] = "never violent"
    elif int(list(campaign.prim_meth.unique())[0]) == 1:
        id_to_violence[id] = "always violent"


# Append the modified violence column to the DataFrame
merged_df['resistance method'] = merged_df['id'].map(id_to_violence)

merged_df.to_csv("Information-Visualization/data/processed_data.csv")

