import os
import sys

file_name = sys.argv[1]
folder_name = "parents"
file_name = file_name + ".txt"

with open(os.path.join(folder_name, file_name), 'r') as f: 

    lines = f.readlines()

    for line in lines:
        
        line = line.strip()
        data = line.split(" ")
        commit_sha = data[0]
        parent_sha = data[1:]
        
        if len(parent_sha) == 0:
            with open("parents.csv", "a") as outfile:
                outfile.write(commit_sha + ",None\n")
        else:
            for p in parent_sha:
                with open("parents.csv", "a") as outfile:
                    outfile.write(commit_sha + "," + p + "\n")


            

