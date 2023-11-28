# Visual Code Revisions: Creating the csvs and populating the database

## For creating the database we have to run the following scripts and python files. The scripts needed to run the python files are provided in the `scripts/creating_the_csvs` folder.

### 1. `extract_renames.py`

This file i) creates the `project_file_revision_commitsha_commitdate_final.csv` file which contains the information about all the Pure Data (PD) revision files, and ii) saves all the parsed contents of the revision files in the `stats_revisions` folder. 

#### Creating the initial version of the revision csv:
If you are running parallel scripts for faster processing, then merge the files to create the final csv, and add appropriate header. For example:

`cat project_file_revision_commitsha_commitdate_1.csv >> project_file_revision_commitsha_commitdate.csv`

`cat project_file_revision_commitsha_commitdate_2.csv >> project_file_revision_commitsha_commitdate.csv`

Add a postprocessing step for replacing the \_COMMA\_ with , to conform with the csv formatting.

`cat project_file_revision_commitsha_commitdate.csv | sed 's/\,/_COMMAFILE_/g' | sed 's/_COMMA_/\,/g' | sed 's/_COMMAFILE_/_COMMA_/g' > project_file_revision_commitsha_commitdate_final.csv`


Add a header line in the merged csv : 
**Project_Name,File,Revision,Commit_SHA,Commit_Date**

1. **Project_Name**: Name of the PD Project
2. **File**: Original PD file name extracted from the commit ids (, in the filename is replaced with \_COMMA\_)
3. **Revision**: Revision file name that is associated with the commit ids of a particular PD file.
4. **Commit_SHA**: Commit ID
5. **Commit_Date**: Date and Time of the commit

#### Saving the parsed content:

The parsed content of the files are saved in the `stats_revisions/<<project_name>>` folders. The filename is in the following format:

`<<original_PD_filename_modified>>_CMMT_<<commit_sha>>.json`

Note that the original pd file name has been modified to replace the **/** sign in the filename to **\_FFF\_** without the extension. To save time in manual post-processing, keep the extension name.


### 2. `create_csvs_for_hash_ids.py`

After creating the parsed contents of the Pure Data files, we move on to saving the hashed values of the parsed contents. We do this by running the create_csvs_for_hash_ids.py file. 

If you are running parallel scripts for faster processing, then merge the files to create the final csv, and add appropriate header. For example:

`cat project_file_commit_hash1.txt >> all_hashes.csv`

`cat project_file_commit_hash2.txt >> all_hashes.csv`

Add a header line in the merged csv : 
**Project_Name,File,Commit_SHA,Hash**

1. **Project_Name**: Name of the PD Project
2. **File**: Original PD file name extracted from the commit ids (, in the filename is replaced with \_COMMA\_)
3. **Commit_SHA**: Commit ID
4. **Hash**: SHA-256 hash value of the parsed contents


### 3. `nodes_edges.py`

This csv saves the nodes and edges information per PD file and per project.

Add a header line in the `nodes_edges_per_file.csv` : 
**Project_Name,File,Commit_SHA,Nodes,Edges**

1. **Project_Name**: Name of the PD Project
2. **File**: Original PD file name extracted from the commit ids (, in the filename is replaced with \_COMMA\_)
3. **Commit_SHA**: Commit ID
4. **Nodes**: Number of nodes in the PD file
5. **Edges**: Number of edges in the PD file


Add a header line in the `nodes_edges_per_project.csv` : 
**Project_Name,Nodes,Edges**

1. **Project_Name**: Name of the PD Project
4. **Nodes**: Number of nodes in the PD project
5. **Edges**: Number of edges in the PD project


### 4. `author_commit_message.sh`

This script creates the csvs responsible for saving the author and commit message information per revision file. For each revision file, we are saving the project_name,commit_sha,author_information, and commit_message. 

If you are running parallel scripts for faster processing, then merge the files to create the final csv, and add appropriate header. For example:

`cat authors1.csv >> authors.csv`

`cat authors2.csv >> authors.csv`

`cat commit_messages1.txt >> commit_messages.txt`

`cat commit_messages2.txt >> commit_messages.txt`

After creating the initial authors and commit messages files, we can create the final csv files (formatted and hashed) needed to load into the database using the following python files:

`create_author_csv.py` and `create_commit_message_csv.py`

Please note that `create_author_csv.py` uses the unique commit_sha and author_informations to create the final csv file. To find the unique commit_sha and author_information you can use `cat authors.csv | cut -d "," -f 2- | sort -u`. The unique commit_sha-commit message csv file is automatically created by the `create_commit_message_csv.py` file.

The final csvs will then contain the following information:

1. `authors_hashed.csv`:

    - **Commit_SHA** : The commit id
    - **Author_Name** : SHA-256 hash value of the author name
    - **Author_Email** : SHA-256 hash value of the author email
    - **Committer_Name** : SHA-256 hash value of the committer name
    - **Committer_Email** : SHA-256 hash value of the committer email

2. `commit_messages_unique.csv`:

    - **Commit_SHA**: The commit id
    - **Commit_Message**: The commit message of the commit id


### 5. `merge_csvs.py`:

After creating all the csv files from the above-mentioned steps, we then merge the necessary csvs to create the final csv which is used to populate the Revision table. We merge the `all_hashes.csv` file with `nodes_edges_per_file.csv` to create the `project_file_commitsha_hash_nodes_edges_final.csv` file. This file is merged again with the `project_file_revision_commitsha_commitdate_final.csv` created in step 1 to create the final csv for the Revision table titled `project_file_revision_commitsha_commitdate_hash_nodes_edges_final.csv`.

1. **Project_Name**: Name of the PD Project
2. **File**: Original PD file name extracted from the commit ids (, in the filename is replaced with \_COMMA\_)
3. **Revision**: Revision file name that is associated with the commit ids of a particular PD file
4. **Commit_SHA**: Commit ID
5. **Commit_Date**: Datetime string of the commit
6. **Hash**: SHA-256 hash value of the parsed contents
7. **Nodes**: Number of nodes in the PD file
8. **Edges**: Number of edges in the PD file




### 6. Populating the database:

After creating all the necessary csvs, we can then create the database by runnning the script in `sqlite/script_for_creating_database.sh`. The python files which are run in this script are:

- `create_new_database.py` : This file creates a new sqlite database called `database.db` and inserts four table in this database called `Projects`, `Revisions`, `Authors`, and `Commit_Messages`. The python file utilizes the csv files created in steps 1-5 to create the tables.
- `update_revisions_and_add_indices.py` : This file adds a DATETIME column of the commit date in the `Revision` table and adds necessary indices.
- `create_hash_table.py` : This file creates a new table called `Hashes`. This table stores the unique SHA-256 hash ids of the parsed revision files along with their parsed contents.
- `create_hash_content.sh` : This file populates the hash table using the saved contents in the `stats_revisions` folder generated from step 1.








