# Opening the Valve on Pure Data: usage of the database

In the following sections, we explain the usage of our dataset. Our dataset is available at https://archive.org/details/Opening_the_Valve_on_Pure_Data. The db file is titled **database.db**. We have also made the mirrored PD repositories available in the same link, the file is titled **pd_mirrored.tar.gz**.

**Please make necessary modification to the folder structure in the scripts to save the files in your desired locations and run `pip install -r requirements.txt` to install the necessary dependencies**

# Structure of our Dataset

Our dataset has seven tables: Revisions, Contents, Authors, Commit_Messages, Commit_Parents, Content_parents, and Projects. The schema of our dataset is shown below:

```
CREATE TABLE "Revisions" (
  "Project_Name" TEXT,
  "File" TEXT,
  "Revision" TEXT,
  "Commit_SHA" TEXT,
  "Commit_Date" TEXT,
  "Hash" TEXT,
  "Nodes" INTEGER,
  "Edges" INTEGER,
  "Commit_DateTime" DATETIME);
CREATE TABLE "Contents" (
  "Hash" TEXT,
  "Content" TEXT
);
CREATE UNIQUE INDEX "ix_Hashes_index" ON "Contents" ("Hash");
CREATE TABLE "Projects" (
"Project_Name" TEXT,
  "Default_Branch" TEXT,
  "Total_Commits" INTEGER
);
CREATE TABLE "Authors" (
"Commit_SHA" TEXT,
  "Author_Name" TEXT,
  "Author_Email" TEXT,
  "Committer_Name" TEXT,
  "Committer_Email" TEXT
);
CREATE TABLE "Commit_Messages" (
"Commit_SHA" TEXT,
  "Commit_Message" TEXT
);
CREATE TABLE "Commit_Parents" (
"Commit_SHA" TEXT,
  "Parent_SHA" TEXT
);
CREATE TABLE "Content_Parents" (
"Project_Name" TEXT,
  "File" TEXT,
  "Commit_SHA" TEXT,
  "Content_Parent_SHA" TEXT
);
CREATE INDEX "ix_Revisions_Hashes_index" ON "Revisions" ("Hash");
CREATE INDEX "ix_Revisions_Projects_index" ON "Revisions" ("Project_Name");
CREATE INDEX "ix_Revisions_Commit_index" ON "Revisions" ("Commit_SHA");
CREATE INDEX "ix_Projects_index" ON "Projects" ("Project_Name");
CREATE INDEX "ix_Authors_index" ON "Authors" ("Commit_SHA");
CREATE INDEX "ix_Commit_Messages_index" ON "Commit_Messages" ("Commit_SHA");
CREATE INDEX "ix_Commit_Parents_index" ON "Commit_Parents" ("Commit_SHA");
CREATE INDEX "ix_Content_Parents_index" ON "Content_Parents" ("Commit_SHA");
```

![Schema of our Dataset](./images/Schema.pdf)

# Usage of our database (database.db)

## 1. How to load the sqlite command line interface
After downloading our database you can query it by using sqlite3 command line tools. **Please note that the size of our database is 21.3GB**, so make sure you have necessary space in your system. You can use sqlite3 (>=3.7.17) to query our database. To load the sqlite3 command line tool and query our database, go to your command line and type `sqlite3 database.db`. This will open up a sqlite3 command line interface for querying our database. Then you can run your SQL queries directly from the command line. Some examples are given below. You can exit sqlite3 the command line interface by running `.exit` on the command line.

Additionally, you can follow [Example 2 of Step 8](#example-2-open-the-sqlite3-command-line-using-a-bash-script) to start the sqlite3 command line interface using our provided bash script.

## 2. Some sample queries

### Example 1: Load three projects with the highest commit count
```
SELECT Project_Name, Total_Commits 
FROM Projects 
ORDER BY Total_Commits DESC 
LIMIT 3;
```

### Example 2: Get all information about a PD file "sampler.pd" from project "zzsnzmn_puredata-sampler"
```
SELECT * 
FROM Revisions 
WHERE Project_Name = "zzsnzmn_puredata-sampler" and File = "sampler.pd";
```

### Example 3: Get the parsed contents of the revision of a PD file "sampler.pd" from project "zzsnzmn_puredata-sampler" where the commit id of the revision is "a2f917add8664dc59ff285ddfb589bc5e9486503"

```
SELECT c.Content 
FROM Contents c 
JOIN Revisions r ON c.Hash = r.Hash 
WHERE r.Project_Name = "zzsnzmn_puredata-sampler" and r.File="sampler.pd" and r.Commit_SHA = "a2f917add8664dc59ff285ddfb589bc5e9486503";
```

Additionally, you can follow [Example 1 of Step 8](#example-1-get-the-contents-of-a-revision-of-a-pd-file-given-project-name-file-name-and-commit-sha-of-that-revision) to run this command directly using our bash script.

### Example 4: Get all authors of the project "zzsnzmn_puredata-sampler" who worked on the PD files
```
SELECT a.Author_Name 
FROM Authors a 
JOIN Revisions r ON a.Commit_SHA = r.Commit_SHA 
WHERE r.Project_Name = "zzsnzmn_puredata-sampler";
```

### Example 5: Get the commit messages of the unique commit IDs of the project "zzsnzmn_puredata-sampler"
```
SELECT DISTINCT(c.Commit_SHA), c.Commit_Message 
FROM Commit_Messages c 
JOIN Revisions r ON c.Commit_SHA = r.Commit_SHA 
WHERE r.Project_Name = "zzsnzmn_puredata-sampler";
```

### Example 6: Get three projects with the highest number of PD files and show their total commit count

```
SELECT
    p.Project_Name,
    p.Total_Commits
FROM
    Projects p
JOIN (
    SELECT
        Project_Name,
        COUNT(DISTINCT File) AS File_Count
    FROM
        Revisions
    GROUP BY
        Project_Name
    ORDER BY
        File_Count DESC
    LIMIT 3
) r ON p.Project_Name = r.Project_Name;
```

## 3. How to get the JSON of a revision of a PD file "sampler.pd" from project "zzsnzmn_puredata-sampler" where the commit id of the revision is "a2f917add8664dc59ff285ddfb589bc5e9486503" using our database
```
SELECT c.Content 
FROM Contents c 
JOIN Revisions r ON c.Hash = r.Hash 
WHERE r.Project_Name = "zzsnzmn_puredata-sampler" and r.File="sampler.pd" and r.Commit_SHA = "a2f917add8664dc59ff285ddfb589bc5e9486503";
```

## 4. How to unzip the git repos (pd_mirrored.tar.gz)
**Note that the pd_mirrored.tar.gz file is 242.5 GB in size**. Please make sure you have sufficient space in your system before unzipping the contents of this tar file.

```
# At first go to your desired directory where you want to save your unzipped folder
cd <destination_folder>

# Then run the following command to unzip the contents of the tar file
tar -xzf pd_mirrored.tar.gz
```

## 5. How to get the raw contents of a PD file revision "sampler.pd" from project "zzsnzmn_puredata-sampler" where the commit id of the revision is "a2f917add8664dc59ff285ddfb589bc5e9486503" using `git show`

```
# Go to the project folder
cd pd_mirrored/zzsnzmn_puredata-sampler

# Then run the following command
git show a2f917add8664dc59ff285ddfb589bc5e9486503:"sampler.pd"
```

The format of this command is: 

`git show <commit_sha>:<revision_of_a_pd_file_name_from_the_Revision_column>`

## 6. How to manually parse the contents of a PD file

Our PD file parser is stored in the `parsing the PD file contents/parsers/pd/pdparser.py` file. We can pass a PD file manually to this parser and get the parsed contents of the file. To get the parsed contents of a PD file, we can run

`python parsing the PD file contents/parse.py <pd_file_name>`

The output will be stored in the `parsing the PD file contents/example PD file and parsed output` folder inside the file `example.json`.


## 7. Understanding the parsed contents

`parsing the PD file contents/example PD file and parsed output/example.json` is an example parsed content of a PD file. We are saving information about nodes and edges in a JSON format in our database. 

- "edges" field represents the number of total connections or edges
- "nodes" field represents the number of total objects or nodes in a PD file
- "node_types" is a dictionary which contains the count of the different types of nodes
- "all_objects" is an array containing the details of each object
- "connections" stores the edge information including source and destination object IDs and the inlet and outlet numbers.


## 8. How to use our provided scripts to run the sql queries easily 

Please put the helper scripts in the same folder as the database.

### Example 1: Get the contents of a revision of a PD file given Project Name, File Name, and Commit SHA of that revision

You can use our provided script `helper scripts for the database/show_file.sh` to get the contents of the file. Run the query mentioned below from your command line after inserting your project name, file name, and commit sha of the revision.

`./show_file.sh <project_name> <file_name> <commit_sha>`

For example:

`./show_file.sh zzsnzmn_puredata-sampler sampler.pd a2f917add8664dc59ff285ddfb589bc5e9486503`

### Example 2: Open the sqlite3 command line using a bash script
Run our script `helper scripts for the database/sqlite.sh` to open the sqlite3 command line interface for querying our database.

`./sqlite.sh`


### Example 3: Run a query directly using a bash script
Run our script `helper scripts for the database/sqlite_query.sh` to open the sqlite3 command line interface for querying our database.

Format: `./sqlite_query.sh <query>`

For example:

`./sqlite_query.sh "Select * from projects where project_name = 'zzsnzmn_puredata-sampler';"`