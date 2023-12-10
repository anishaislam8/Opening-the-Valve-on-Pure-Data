# Opening the Valve on Pure Data: Collecting the data, creating the csvs, populating the database, and the usage of the database

This project contains the scripts for creating a dataset for Pure Data (PD), which consists of the following components: scripts for i) collecting the data from the World of Code, ii) collecting commit information incuding commit messages, author and committer information, commit parents, and content parents, iii) constructing the database. In the following sections, we explain the usage of our database and steps for replicating our work

**Please make necessary modification to the folder structure in the scripts to save the files in your desired locations and run `pip install -r requirements.txt` to install the necessary dependencies**


# Usage of our database (revision_hashes.db)

## 1. How to load the sqlite command line interface
After downloading our database you can query it by using sqlite3 command line tools. **Please note that the size of our database is 36.6GB**, so make sure you have necessary space in your system. You can use sqlite3 (>=3.7.17) to query our database. To load the sqlite3 command line tool and query our database, go to your command line and type `sqlite3 revision_hashes.db`. This will open up a sqlite3 command line interface for querying our database. Then you can run your SQL queries directly from the command line. Some examples are given below. You can exit sqlite3 the command line interface by running `.exit` on the command line.

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

Our PD file parser is stored in the `parsers/pd/pdparser.py` file. We can pass a PD file manually to this parser and get the parsed contents of the file. To get the parsed contents of a PD file, we can run

`python parse.py <pd_file_name>`

The output will be stored in the example folder inside the file `example.json`.


## 7. Understanding the parsed contents

`example/example.json` is an example parsed content of a PD file. We are saving information about nodes and edges in a JSON format in our database. 

- "edges" field represents the number of total connections or edges
- "nodes" field represents the number of total objects or nodes in a PD file
- "node_types" is a dictionary which contains the count of the different types of nodes
- "all_objects" is an array containing the details of each object
- "connections" stores the edge information including source and destination object IDs and the inlet and outlet numbers.

Note that, in our database, in addition to the above mentioned fields, we have stored two more fields for the commit sha and commit date associated with the revision of the PD file that generates this content.

## 8. How to use our provided scripts to run the sql queries easily 

Please put the helper scripts in the same folder as the database.

### Example 1: Get the contents of a revision of a PD file given Project Name, File Name, and Commit SHA of that revision

You can use our provided script `helper scripts/show_file.sh` to get the contents of the file. Run the query mentioned below from your command line after inserting your project name, file name, and commit sha of the revision.

`./show_file.sh <project_name> <file_name> <commit_sha>`

For example:

`./show_file.sh zzsnzmn_puredata-sampler sampler.pd a2f917add8664dc59ff285ddfb589bc5e9486503`

### Example 2: Open the sqlite3 command line using a bash script
Run our script `helper scripts/sqlite.sh` to open the sqlite3 command line interface for querying our database.

`./sqlite.sh`


### Example 3: Run a query directly using a bash script
Run our script `helper scripts/sqlite_query.sh` to open the sqlite3 command line interface for querying our database.

Format: `./sqlite_query.sh <query>`

For example:

`./sqlite_quey.sh "Select * from projects where project_name = 'zzsnzmn_puredata-sampler';"`


# Replicating our work
## Step 1: Collecting the data from the World of Code.

1. At first extract the pure data blobs and files from the World of Code using the following command: 
    
    `zcat /da?_data/basemaps/gz/b2fFullU*.s | grep -i '\.pd$' | sort -u >> pd_blobs_files.txt`

2. Then, extract the blob IDs only:

    `cat pd_blobs_files.txt | cut -d ";" -f 1 | sort -u >> pd_blobs.txt`

3. Get the contents of the blobs using the script `scripts/pd_blob_contents.sh`

4. Filter the contents of the PD blobs to extract the actual PD blobs using the following command:

    `grep -irl "\#N " | cut -d "." -f 1 >> ../actual_pd_blobs.txt`

5. Get the project names using the script `scripts/pd_project_extraction.sh`

6. Commands for creating the final project files (to fix some formatting):
    ```
    cat pd_projects_new.txt | grep -v ";" | sort -u >> pd_projects_1.txt
    cat pd_projects_new.txt | grep ";" | sed -n 's/;/\n/gp' | sort -u >> pd_projects_2.txt
    cat pd_projects_1.txt >> pd_projects_all.txt
    cat pd_projects_2.txt >> pd_projects_all.txt
    cat pd_projects_all.txt | sort -u >> pd_projects_final.txt
    ```

7. Run the `scripts/project_files.sh` to get file names of the current repository.

8. Command for getting project names that has a .pd file in the file list:
    
    `grep -irl '\.pd$' | sort -u | sed 's/\.[^.]*$//' >> ../pd_projects_final.txt`

After following the the commands in step 1, your final PD projects names will be in the `pd_projects_final.txt` file.
    
## Step 2: Download the mirror repositories and extract the default branch.

Run the `scripts/mirrored_repo_and_branch.sh` to download the mirrored repo of the PD projects and to get the default branch name. Your final project names and their default branch names will be stored in the `branch_name_CORRECT.csv` file.

## Step 3: Extract author information and commit messages

Run `scripts/creating_the_csvs/author_commit_message.sh` to extract the author and commit messages of all the cloned projects. 

This script creates the csvs responsible for saving the author and commit message information per revision file. For each revision file, we are saving the project_name,commit_sha,author_information, and commit_message. 

If you are running parallel scripts for faster processing, then merge the files to create the final csv, and add appropriate header. For example:

```
cat authors1.csv >> authors.csv
cat authors2.csv >> authors.csv
cat commit_messages1.txt >> commit_messages.txt
cat commit_messages2.txt >> commit_messages.txt
```

After creating the initial authors and commit messages files, we can create the final csv files (formatted and hashed) needed to load into the database using the following commands and python files:

### Author information extraction

 - At first find the unique lines in the `authors.csv` file using `cat authors.csv | sort -u > authors_projects_unique.csv`.

 - Then we filter out the unidentified or invalid author information by searching for the ,**=\_COMMA\_=\_COMMA\_=\_COMMA\_=** syntax and **unknown\_COMMA\_=\_COMMA\_unknown\_COMMA\_=** syntax in the `authors_projects_unique.csv` file using the following commands:

    `cat authors_projects_unique.csv | grep -v unknown_COMMA_=_COMMA_unknown_COMMA_= | grep -v =_COMMA_=_COMMA_=_COMMA_= > authors_projects_unique_filtered.csv`

- After that, run `create_filtered_author_csv.py`to get the hashed author information of the filtered author info and save the output in `authors_projects_unique_filtered_hashed.csv`.

- Finally, get the final author csv by running

    `cat authors_projects_unique_filtered_hashed.csv | cut -d "," -f 2- | sort -u > authors_filtered_hashed.csv`

- Add appropriate header to this file: 
    `Commit_SHA,Author_Name,Author_Email,Committer_Name,Committer_Email` 


### Commit messages extraction
Run the `create_commit_message_csv.py`and the final csv file for commit messages will be automatically stored in `commit_messages_unique.csv`

The final csvs will then contain the following information:

1. `authors_filtered_hashed.csv`:

    - **Commit_SHA** : The commit id
    - **Author_Name** : SHA-256 hash value of the author name
    - **Author_Email** : SHA-256 hash value of the author email
    - **Committer_Name** : SHA-256 hash value of the committer name
    - **Committer_Email** : SHA-256 hash value of the committer email

2. `commit_messages_unique.csv`:

    - **Commit_SHA**: The commit id
    - **Commit_Message**: The commit message of the commit id


## Step 4: Extract commit parents and content parents

### Extracting commit parents
- At first run `scripts/creating_the_csvs/extract_parent_commit.sh` to extract the parent commits for all commits in each of the projects.

- Then, run `create_commit_parent_table.py` to create the `parents.csv` file (Merge the csvs in the case of parallel execution for faster processing)

- After that, run  `cat parents.csv | sort -u > parents_unique.csv` to get the final csv file that you can load into the database. Add necessary header line `Commit_SHA,Parent_SHA`

This csv contains:

- **Commit_SHA** : The commit ID
- **Commit_Parent** : The parent commit ID

**At this stage, add this table to the database by running the commit parent specific lines (df5) from the `sqlite/add_new_tables.py` file.**

### Extracting content parents

Run `create_content_parents_csv.py` to easily access our database and create the `content_parents.csv` file which can be used to load into the database for creating the Content_Parents table.

Add appropriate header after generating the csv: `Project_Name,File,Commit_SHA,Content_Parent_SHA`

This csv contains:

- **Project_Name** : The project Name
- **File** : The PD file name
- **Commit_SHA** : The commit ID
- **Content_Parent_SHA** : The content parent commit ID


## Step 5: Extracting the total number of commits
- Run the `scripts/creating_the_csvs/total_commits.sh` to generate the `total_commits.csv` file.

- Merge this csv with the `sqlite/csvs/branch_name_CORRECT.csv` using `create_projects_csv.py`. This python file will generate `projects.csv` file which we can use to populate the `Projects` table in our database.

This csv contains:
- **Project_Name** : The project Name
- **Default_Branch** : The default branch name
- **Total_Commits** : Total number of commits in the projects


## Step 6: Populating the database

For populating the remaining tables in the database, we follow the following steps:

1. `Revisions` and `Contents`: To populate these two tables directly in our database, at first run the `sqlite/create_content_table.py`. This python file will create these two tables in our database and add unique index in the `Hash` column of the contents table.

    Next, we use the `sqlite/extract_renames_db.py` file. This python file will calculate the revisions for each PD files for all the projects, parse the contents of the revisions of the PD files, and populate the `Revisions` and `Contents` table accordingly. Note that, the file name and the revision of the PD file name is formatted to replace the , to \_COMMA\_.

2. `Authors`, `Commit_Messages`, `Content_Parents`, `Projects`: Run the `sqlite/add_new_tables.py` file for inserting these tables in the database.

3. `Commit_Parents`: Already inserted in [Step 4](#extracting-commit-parents).

To Add necessary indices in our database, run `sqlite/update_revisions_and_add_indices.py`.This file adds a DATETIME column of the commit date in the `Revision` table and adds necessary indices to the existing tables.


## Step 7: Answering the research questions
We can answer our research questions by finding differences in the number of nodes and edges between each commit and their content parents by running `differences_in_nodes_and_edges.py`. This file will create a file called `differences_final.csv` which we can use to answer our research questions. 








