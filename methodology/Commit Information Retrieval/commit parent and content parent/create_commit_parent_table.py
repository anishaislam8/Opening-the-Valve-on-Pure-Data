import sqlite3
import pandas as pd

# step 1: load data file
df = pd.read_csv('../../../csvs/parents_unique.csv')


# step 2: clean data
df.columns = df.columns.str.strip()

# step 3: create/connect to database (please fix the path to the database file)
connection = sqlite3.connect("database.db")
c = connection.cursor()

# step 4: load data file to sqlite
df.to_sql("Commit_Parents", connection, if_exists='replace', index=False)

c.execute('''CREATE INDEX "ix_Commit_Parents_index" ON "Commit_Parents" ("Commit_SHA");''')

# step 5: close connection
connection.commit()
connection.close()