# How to collect the project names from the world of code

You can find all the necessary scripts mentioned below for collecting the project names inside this directory.

## Step 1: Collecting the data from the World of Code.

1. At first extract the pure data blobs and files from the World of Code using the following command: 
    
    `zcat /da?_data/basemaps/gz/b2fFullU*.s | grep -i '\.pd$' | sort -u >> pd_blobs_files.txt`

2. Then, extract the blob IDs only:

    `cat pd_blobs_files.txt | cut -d ";" -f 1 | sort -u >> pd_blobs.txt`

3. Get the contents of the blobs using the script `pd_blob_contents.sh`

4. Filter the contents of the PD blobs to extract the actual PD blobs using the following command:

    `grep -irl "\#N " | cut -d "." -f 1 >> ../actual_pd_blobs.txt`

5. Get the project names using the script `pd_project_extraction.sh`

6. Commands for creating the final project files (to fix some formatting):
    ```
    cat pd_projects_new.txt | grep -v ";" | sort -u >> pd_projects_1.txt
    cat pd_projects_new.txt | grep ";" | sed -n 's/;/\n/gp' | sort -u >> pd_projects_2.txt
    cat pd_projects_1.txt >> pd_projects_all.txt
    cat pd_projects_2.txt >> pd_projects_all.txt
    cat pd_projects_all.txt | sort -u >> pd_projects_final.txt
    ```

7. Run the `project_files.sh` to get file names of the current repository.

8. Command for getting project names that has a .pd file in the file list:
    
    `grep -irl '\.pd$' | sort -u | sed 's/\.[^.]*$//' >> ../pd_projects_final.txt`

After following the the commands in step 1, your final PD projects names will be in the `pd_projects_final.txt` file.
    
## Step 2: Download the mirror repositories and extract the default branch.

Run the `mirrored_repo_and_branch.sh` to download the mirrored repo of the PD projects and to get the default branch name. Your final project names and their default branch names will be stored in the `branch_name_CORRECT.csv` file.
