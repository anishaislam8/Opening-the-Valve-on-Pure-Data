import sqlite3

connection = sqlite3.connect("database.db")
c = connection.cursor()

# # create the table
c.execute('''CREATE TABLE "Revisions" (
  "Project_Name" TEXT,
  "File" TEXT,
  "Revision" TEXT,
  "Commit_SHA" TEXT,
  "Commit_Date" TEXT,
  "Hash" TEXT,
  "Nodes" INTEGER,
  "Edges" INTEGER
);''')


c.execute('''CREATE TABLE "Contents" (
  "Hash" TEXT,
  "Content" TEXT
);''')

# # commit changes
connection.commit()

c.execute('''CREATE UNIQUE INDEX "ix_Hashes_index" ON "Contents" ("Hash");''')
connection.commit()

# # close connection
connection.close()