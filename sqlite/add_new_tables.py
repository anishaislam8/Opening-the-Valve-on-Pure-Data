import sqlite3
import pandas as pd

# step 1: load data file
df = pd.read_csv('csvs/projects.csv')
df3 = pd.read_csv('csvs/authors_filtered_hashed.csv')
df4 = pd.read_csv('csvs/commit_messages_unique.csv')
#df5 = pd.read_csv('csvs/parents_unique.csv')
df6 = pd.read_csv('csvs/content_parents.csv')

# step 2: clean data
df.columns = df.columns.str.strip()
df3.columns = df3.columns.str.strip()
df4.columns = df4.columns.str.strip()
#df5.columns = df5.columns.str.strip()
df6.columns = df6.columns.str.strip()

# step 3: create/connect to database
connection = sqlite3.connect("revision_hashes.db")

# step 4: load data file to sqlite
df.to_sql("Projects", connection, if_exists='replace', index=False)
df3.to_sql("Authors", connection, if_exists='replace', index=False)
df4.to_sql("Commit_Messages", connection, if_exists='replace', index=False)
#df5.to_sql("Commit_Parents", connection, if_exists='replace', index=False)
df6.to_sql("Content_Parents", connection, if_exists='replace', index=False)



# step 5: close connection
connection.commit()
connection.close()



