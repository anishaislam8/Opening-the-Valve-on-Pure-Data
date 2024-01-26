# How to collect the project names from the world of code

## Step 1: Collecting the data from the World of Code.

1. At first, extract the pure data blobs and files from the World of Code using the following command: 
    
    `zcat /da?_data/basemaps/gz/b2fFullU*.s | grep -i '\.pd$' | sort -u >> pd_blobs_files.txt`

2. Then, extract the blob IDs only:

    `cat pd_blobs_files.txt | cut -d ";" -f 1 | sort -u >> pd_blobs.txt`

3. Get the contents of the blobs using the command `./pd_blob_contents.sh`

4. Filter the contents of the PD blobs to extract the actual PD blobs using the following command inside the *pd_blobs_new* directory generated in step 3:

    `grep -irl "\#N " | cut -d "." -f 1 >> ../actual_pd_blobs.txt`

5. Get the project names by running `./pd_project_extraction.sh`

6. Commands for creating the penultimate project files (to fix some formatting):
    ```
    cat pd_projects_new.txt | grep -v ";" | sort -u >> pd_projects_1.txt
    cat pd_projects_new.txt | grep ";" | sed -n 's/;/\n/gp' | sort -u >> pd_projects_2.txt
    cat pd_projects_1.txt >> pd_projects_all.txt
    cat pd_projects_2.txt >> pd_projects_all.txt
    cat pd_projects_all.txt | sort -u >> pd_projects_temp.txt
    ```

7. Download the projects mentioned in the *pd_projects_temp.txt* file from GitHub and save them in a new directory called *pd_projects*. The command for downloading a particular repository from GitHub is as follows:

    `git clone https://:@github.com/<project_name> pd_projects/<project_name>`

To get a list of the downloaded projects, run `ls pd_projects | wc -l > downloaded_pd_projects.txt`

8. Run the command `./project_files.sh` to get the file names of the current repository.

9. Command for getting project names that have a .pd file in the file list from the *pd_git_files* directory created in step 8:
    
    `grep -irl '\.pd$' | sort -u | sed 's/\.[^.]*$//' >> ../pd_projects_final.txt`

After following the commands in step 1, your final PD project names will be in the `pd_projects_final.txt` file.
    
## Step 2: Download the mirror repositories and extract the default branch.

Run the command `./mirrored_repo_and_branch.sh` to download the mirrored repository of the PD projects and to get the default branch name. Your final project names and their default branch names will be stored in the *branch_name_CORRECT.csv* file.
