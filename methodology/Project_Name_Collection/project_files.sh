#!/bin/bash
mkdir pd_git_files
INPUT=downloaded_pd_projects.txt
while read p; do
    cd pd_projects/$p
    branch=`git rev-parse --abbrev-ref HEAD`
    git ls-tree -r --name-only $branch >> pd_git_files/$p.txt
done < $INPUT