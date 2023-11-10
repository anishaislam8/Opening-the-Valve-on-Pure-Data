import sqlite3
import pandas as pd

# step 1: load data file
df = pd.read_csv('/data/play/aislam4/thesis/pd_parsed/csvs/branch_name_CORRECT.csv')
df2 = pd.read_csv('/data/play/aislam4/thesis/pd_parsed/csvs/project_file_revision_commitsha_commitdate_hash_final.csv')

# step 2: clean data
df.columns = df.columns.str.strip()
df2.columns = df2.columns.str.strip()

# step 3: create/connect to database
connection = sqlite3.connect("/data/play/aislam4/thesis/pd_parsed/sqlite/database.db")

# step 4: load data file to sqlite
df.to_sql("Projects", connection, if_exists='replace', index=True)
df2.to_sql("Revisions", connection, if_exists='replace', index=True)

# step 5: close connection
connection.close()


