INPUT=project_name.txt
while read p; do
    python3 /parents_scripts/create_commit_parent_csv.py $p
done < $INPUT

