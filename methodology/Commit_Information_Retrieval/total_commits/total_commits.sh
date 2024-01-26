#!/bin/bash
# Please use only the project names from the branch_name_CORRECT.csv file as input for this script.

INPUT=../../../csvs/project_name.csv
while read p; do
    cd /pd_mirrored_extracted/$p
    size=`git --no-pager log --all --pretty=tformat:"%H %P" | wc -l`
    echo $p,$size >> total_commits.txt
done < $INPUT