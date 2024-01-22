import pandas as pd

# fix the location as needed
df = pd.read_csv('../../../csvs/total_commits.csv')
df2 = pd.read_csv('../../../csvs/branch_name_CORRECT.csv')
merged_df2 = pd.merge(df2, df, on=['Project_Name'])

# save the dataframe df2 to a csv file
merged_df2.to_csv('csvs/projects.csv', index=False)