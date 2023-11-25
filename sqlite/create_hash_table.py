import sqlite3

#folder = sys.argv[1]
#folder_name = "/pd_parsed/stats_revisions/" + folder

connection = sqlite3.connect("database.db")
c = connection.cursor()

# # create the table
c.execute('''CREATE TABLE "Hashes" (
  "Hash" TEXT,
  "Content" TEXT
);''')

# # commit changes
connection.commit()

c.execute('''CREATE UNIQUE INDEX "ix_Hashes_index" ON "Hashes" ("Hash");''')
connection.commit()

# # close connection
connection.close()
