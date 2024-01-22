# Extract commit related information

You can find all the necessary scripts mentioned below for extracting the commit information inside this directory.


## Step 1: Extract author information and commit messages

Run `./author and commit message/author_commit_message.sh` to extract the author and commit messages of all the cloned projects. 

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

- After that, run `./author and commit message/create_filtered_author_csv.py`to get the hashed author information of the filtered author info and save the output in `authors_projects_unique_filtered_hashed.csv`.

- Finally, get the final author csv by running

    `cat authors_projects_unique_filtered_hashed.csv | cut -d "," -f 2- | sort -u > authors_filtered_hashed.csv`

- Add appropriate header to this file: 
    `Commit_SHA,Author_Name,Author_Email,Committer_Name,Committer_Email` 


### Commit messages extraction
Run the `./author and commit message/create_commit_message_csv.py`and the final csv file for commit messages will be automatically stored in `commit_messages_unique.csv`

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


## Step 2: Extract commit parents and content parents

### Extracting commit parents
- At first run `./commit parent and content parent/extract_parent_commits.sh` to extract the parent commits for all commits in each of the projects.

- Then, run `./commit parent and content parent/create_commit_parent_csv.py` to create the `parents.csv` file (Merge the csvs in the case of parallel execution for faster processing)

- After that, run  `cat parents.csv | sort -u > parents_unique.csv` to get the final csv file that you can load into the database. Add necessary header line `Commit_SHA,Parent_SHA`

This csv contains:

- **Commit_SHA** : The commit ID
- **Commit_Parent** : The parent commit ID

**At this stage, add this table to the database by running the `./commit parent and content parent/create_commit_parent_table.py` file.**

### Extracting content parents

Run `./commit parent and content parent/create_content_parents_csv.sh` to easily access our database and create the `content_parents.csv` file which can be used to load into the database for creating the Content_Parents table.

Add appropriate header after generating the csv: `Project_Name,File,Commit_SHA,Content_Parent_SHA`

This csv contains:

- **Project_Name** : The project Name
- **File** : The PD file name
- **Commit_SHA** : The commit ID
- **Content_Parent_SHA** : The content parent commit ID


## Step 3: Extracting the total number of commits
- Run the `./total_commits/total_commits.sh` to generate the `total_commits.csv` file.

- Merge this csv with the `csvs/branch_name_CORRECT.csv` using `./total_commits/create_projects_csv.py`. This python file will generate `projects.csv` file which we can use to populate the `Projects` table in our database.

This csv contains:
- **Project_Name** : The project Name
- **Default_Branch** : The default branch name
- **Total_Commits** : Total number of commits in the projects

