#!/bin/bash

# Check if all three arguments are provided
if [ "$#" -ne 3 ]; then
    echo "Incorrect number of arguments. Usage: $0 <project_name> <file_name> <commit_sha>"
    exit 1
fi

query="SELECT c.Content
FROM Contents c
JOIN Revisions r ON c.Hash = r.Hash
WHERE r.Project_Name = \"${1}\" and r.File= \"${2}\" and r.Commit_SHA = \"${3}\";"

# Execute query and retrieve results
result=$(sqlite3 revision_hashes.db "$query")
echo $result