INPUT=project_name.txt
while read p; do
    python3 /parents_scripts/create_commit_parent_table_contents.py $p
done < $INPUT

