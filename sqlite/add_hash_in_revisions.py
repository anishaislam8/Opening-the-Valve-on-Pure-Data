import pandas as pd

# load the csv files as dataframes
df = pd.read_csv('/data/play/aislam4/thesis/pd_parsed/csvs/all_hashes.csv')
df2 = pd.read_csv('/data/play/aislam4/thesis/pd_parsed/csvs/project_file_revision_commitsha_commitdate_final.csv')
merged_df = pd.merge(df2, df, on=['Commit_SHA', 'Project_Name', 'File'])


# save the dataframe df2 to a csv file
merged_df.to_csv('/data/play/aislam4/thesis/pd_parsed/csvs/project_file_revision_commitsha_commitdate_hash_final.csv', index=False)
