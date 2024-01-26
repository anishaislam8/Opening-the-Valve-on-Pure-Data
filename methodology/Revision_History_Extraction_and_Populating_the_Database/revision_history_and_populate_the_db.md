# Extracting Revision History and Populating the database

For populating the remaining tables in the database, we follow the following steps:

1. `Revisions` and `Contents`: To populate these two tables directly in our database, at first run the command `python3 create_revisions_and_contents_table.py`. This python file will create these two tables in our database and add a unique index in the `Hash` column of the contents table. The table structures are as follows:

- Revisions:
    - **Project_Name** (TEXT): Name of the project
    - **File** (TEXT): Name of the PD file
    - **Revision** (TEXT): Name of the revision of the PD file for a particular commit
    - **Commit_SHA** (TEXT): Commit SHA
    - **Commit_Date** (TEXT): Commit date
    - **Hash** (TEXT): SHA-256 hash value of the content of the revision of the PD file
    - **Nodes** (INTEGER): Number of nodes in the revision of the PD file
    - **Edges** (INTEGER): Number of edges in the revision of the PD file

- Contents:
    - **Hash** (TEXT): SHA-256 hash value of the content of the revision of the PD file
    - **Content** (TEXT): Content of the revision of the PD file

    Next, we run `./extract_revisions.sh` to extract the revisions of each PD file for all the projects, parse the contents of the revisions of the PD files, and populate the `Revisions` and `Contents` tables accordingly. Note that the file name and the revision of the PD file name are formatted to replace , to \_COMMA\_.

2. `Authors`, `Commit_Messages`, `Content_Parents`, `Projects`: Run the `add_remaining_tables.py` file to insert these tables in the database.

3. `Commit_Parents`: Already inserted in the methodology step.

To Add necessary indices in our database, run `python3 update_revisions_and_add_indices.py`. This file adds a DATETIME column of the commit date in the `Revision` table and necessary indices to the existing tables.
