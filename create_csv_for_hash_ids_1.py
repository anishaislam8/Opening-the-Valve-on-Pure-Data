import json
import os
import sys
import hashlib

# source of calculate_sha256(): https://unogeeks.com/python-sha256/#:~:text=In%20Python%2C%20you%20can%20use,represented%20as%20a%20hexadecimal%20string.&text=%23%20Example%20usage%3A,%3D%20%22Hello%2C%20World!%22
def calculate_sha256(data):
    # Convert data to bytes if it’s not already
    if isinstance(data, str):
        data = data.encode()

    # Calculate SHA-256 hash
    sha256_hash = hashlib.sha256(data).hexdigest()

    return sha256_hash

folder= sys.argv[1]
print(folder)
folder_name = "/data/play/aislam4/thesis/pd_parsed/stats_revisions/" + folder


for filename in os.listdir(folder_name):
    
    with open(os.path.join(folder_name, filename), 'r') as f: # open in readonly mode
        # read the json file
        original_part = filename.split("_CMMT_")[0]
        new_original_file_name = original_part.replace(",", "_COMMA_")
        new_original_file_name = new_original_file_name.replace("_FFF_", "/")  
        # suggestion: use the original file name extension and check if the filename is actually empty, in that case, no need to add extensions.    
        new_original_file_name_pd = new_original_file_name + ".pd" 
        
        commit = filename.split("_CMMT_")[1].split(".json")[0]
        if os.stat(os.path.join(folder_name, filename)).st_size != 0:
            
            data = json.load(f)
            
            # convert data to string and assign to content column
            content = str(data)
            
            # calculate the hash value of the content
            hash_value = calculate_sha256(content)

            # assign the folder name to the project_name column
            project_name = folder

            # assign the filename to the file_name column
            file_name = new_original_file_name_pd

            # assign the commit to the commit_sha column
            commit_sha = commit

            with open("/data/play/aislam4/thesis/pd_parsed/csvs/redo/project_file_commit_hash1.txt", "a") as outfile:
                outfile.write("{},{},{},{}\n".format(project_name, file_name, commit_sha, hash_value))

            


