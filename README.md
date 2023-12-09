# Visual Code Revisions: Collecting the data, creating the csvs and populating the database

This project contains the scripts for creating a dataset for Pure Data (PD), which consists of the following components: scripts for i) collecting the data from the World of Code, ii) collecting commit information incuding commit messages, author and committer information, commit parents and content parents, iii) constructing the database. 

**Please make necessary modification to the folder structure in the scripts to save the files in your desired locations and tun `pip install -r requirements.txt` to install the necessary dependencies**


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
    
    `cat pd_projects_new.txt | grep -v ";" | sort -u >> pd_projects_1.txt`

    `cat pd_projects_new.txt | grep ";" | sed -n 's/;/\n/gp' | sort -u >> pd_projects_2.txt`

    `touch pd_projects_all.txt`

    `cat pd_projects_1.txt >> pd_projects_all.txt`

    `cat pd_projects_2.txt >> pd_projects_all.txt`

    `cat pd_projects_all.txt | sort -u >> pd_projects_final.txt`

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

`cat authors1.csv >> authors.csv`

`cat authors2.csv >> authors.csv`

`cat commit_messages1.txt >> commit_messages.txt`

`cat commit_messages2.txt >> commit_messages.txt`

After creating the initial authors and commit messages files, we can create the final csv files (formatted and hashed) needed to load into the database using the following commands and python files:

### Author information extraction

 - At first find the unique lines in the `authors.csv` file using `cat authors.csv | sort -u > authors_projects_unique.csv`.

 - Then we filter out the unidentified or invalid author information by searching for the ,**=\_COMMA\_=\_COMMA\_=\_COMMA\_=** syntax and **unknown_COMMA_=_COMMA_unknown_COMMA_=** syntax in the `authors_projects_unique.csv` file using the following commands:

    `cat authors_projects_unique.csv | grep -v unknown_COMMA_=_COMMA_unknown_COMMA_= | grep -v =_COMMA_=_COMMA_=_COMMA_= > authors_projects_unique_filtered.csv`

- After that, run `create_filtered_author_csv.py`to get the hashed author information of the filtered author info and save the output in `authors_projects_unique_filtered_hashed.csv`.

- Finally, get the final author csv by running

    `cat authors_projects_unique_filtered_hashed.csv | cut -d "," -f 2- | sort -u > authors_filtered_hashed.csv`

- - Add appropriate header to this file: 
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

**At this stage, add this table to the database by selecting the commit parent specific entries (df5) from the `sqlite/add_new_tables.py` file.**

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

1. `Revisions` and `Contents`: To populate these two tables directly in our database, at first run the sqlite/`create_content_table.py`. This python file will create these two tables in our database and add unique indices in the `Hash` column of the contents table.

    Next, we use the `sqlite/extract_renames_db.py` file. This python file will calculate the revisions for each PD files for all the projects, parse the contents of the revisions of the PD files, and populate the `Revisions` and `Contents` table accordingly.

2. `Authors`, `Commit_Messages`, `Content_Parents`, `Projects`: Run the `sqlite/add_new_tables.py` file for inserting these tables in the database.

3. `Commit_Parents`: Already inserted in Step 4.

To Add necessary indices in our database, run `sqlite/update_revisions_and_add_indices.py`.This file adds a DATETIME column of the commit date in the `Revision` table and adds necessary indices to the existing table.


<!-- 
## Step 7: Data Analysis

After constructing our database, we can run `sqlite/data_analysis.py` to get the statistics of our database and generate the necessary figures. -->


## Step 7: Answering the research questions
We can answer our research questions by finding differences in the number of nodes and edges between each commit and their content parents by running `differences_in_nodes_and_edges.py`. This file will create a file called `differences_final.csv` which we can use to answer our research questions. 
<!-- We can run `sqlite/rq_analysis.py` to get the results of our research questions and generate figures. -->







