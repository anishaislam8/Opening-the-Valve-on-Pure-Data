#!/bin/bash
# Please use only the project names from the branch_name_CORRECT.csv file as input for this script.
mkdir parents
INPUT=../../../csvs/project_name.csv
while read p; do
    cd /pd_mirrored_extracted/$p
    git --no-pager log --all --pretty=tformat:"%H %P" > parents/$p.txt
done < $INPUT
