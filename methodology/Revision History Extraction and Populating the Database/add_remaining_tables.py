import sqlite3
import pandas as pd

# step 1: load data file
df = pd.read_csv('csvs/projects.csv')
df2 = pd.read_csv('csvs/authors_filtered_hashed.csv')
df3 = pd.read_csv('csvs/commit_messages_unique.csv')
df4 = pd.read_csv('csvs/content_parents.csv')

# step 2: clean data
df.columns = df.columns.str.strip()
df2.columns = df2.columns.str.strip()
df3.columns = df3.columns.str.strip()
df4.columns = df4.columns.str.strip()

# step 3: create/connect to database
connection = sqlite3.connect("database.db")


# step 4: load data file to sqlite
df.to_sql("Projects", connection, if_exists='replace', index=False)
df2.to_sql("Authors", connection, if_exists='replace', index=False)
df3.to_sql("Commit_Messages", connection, if_exists='replace', index=False)
df4.to_sql("Content_Parents", connection, if_exists='replace', index=False)

# step 5: close connection
connection.commit()
connection.close()