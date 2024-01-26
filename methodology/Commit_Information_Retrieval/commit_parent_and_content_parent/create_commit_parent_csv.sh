#!/bin/bash
# Please use only the project names from the branch_name_CORRECT.csv file as input for this script.

INPUT=../../../csvs/project_name.csv
while read p; do
    python3 create_commit_parent_csv.py $p
done < $INPUT

