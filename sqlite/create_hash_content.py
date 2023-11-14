import json
import os
import sys
import pandas as pd
import pysqlite3
import subprocess
import hashlib
#import time

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

connection = pysqlite3.connect("database.db")
c = connection.cursor()
c.execute('BEGIN TRANSACTION')
#start = time.process_time()
for filename in os.listdir(folder_name):
    # print(filename)
    with open(os.path.join(folder_name, filename), 'r') as f: # open in readonly mode
        # read the json file
        original_part = filename.split("_COMMIT_")[0]
        fname1 = subprocess.run(['echo "{}"'.format(original_part)], stdout=subprocess.PIPE, shell=True)
        fname2 = subprocess.run(["sed 's/\,/_COMMA_/g'"], input=fname1.stdout, stdout=subprocess.PIPE, shell=True)
        fname3 = subprocess.run(["sed 's/_FOLDER_/\//g'"], input=fname2.stdout, stdout=subprocess.PIPE, shell=True)
        new_original_file_name = fname3.stdout.decode().strip()      
        new_original_file_name_pd = new_original_file_name + ".pd" 
        
        commit = filename.split("_COMMIT_")[1].split(".json")[0]
        if os.stat(os.path.join(folder_name, filename)).st_size != 0:
            
            data = json.load(f)
            
            # convert data to string and assign to content column
            content = str(data)
            
            # calculate the hash value of the content
            hash_value = calculate_sha256(content)
            
            c.execute("INSERT INTO Hashes (Hash, Content) VALUES(?,?) ON CONFLICT(Hash) DO NOTHING", (hash_value, content))


    
connection.commit()
connection.close()


#print(time.process_time() - start)
            

