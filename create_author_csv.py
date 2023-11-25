# This script is run after we extract the unique commit_id,author_info pairs from the authors.csv file.
import pandas as pd
import hashlib

filename = "/pd_parsed/author_commit_message/author/authors_unique.csv"

commits = []
author_names = []
author_emails = []
committer_names = []
committer_emails = []

# source of calculate_sha256(): https://unogeeks.com/python-sha256/#:~:text=In%20Python%2C%20you%20can%20use,represented%20as%20a%20hexadecimal%20string.&text=%23%20Example%20usage%3A,%3D%20%22Hello%2C%20World!%22
def calculate_sha256(data):
    # Convert data to bytes if it’s not already
    if isinstance(data, str):
        data = data.encode()

    # Calculate SHA-256 hash
    sha256_hash = hashlib.sha256(data).hexdigest()

    return sha256_hash

with open(filename, 'r', encoding="utf-8", errors='ignore') as f: # open in readonly mode
        # read the json file
    lines = f.readlines()

    for line in lines:
        # convert data to string and assign to content column
        content = line.split(",")
        
        commit = content[0]
        author_info = content[1]
        author_name = calculate_sha256(author_info.split("_COMMA_")[0])
        author_email = calculate_sha256(author_info.split("_COMMA_")[1])
        committer_name = calculate_sha256(author_info.split("_COMMA_")[2])
        committer_email = calculate_sha256(author_info.split("_COMMA_")[3])        

        
        commits.append(commit)
        author_names.append(author_name)
        author_emails.append(author_email)
        committer_names.append(committer_name)
        committer_emails.append(committer_email)


df = pd.DataFrame(list(zip(commits, author_names, author_emails, committer_names, committer_emails)), columns =['Commit_SHA', 'Author_Name', 'Author_Email', 'Committer_Name', 'Committer_Email'])
df.to_csv("/pd_parsed/csvs/authors_hashed.csv", index=False)

