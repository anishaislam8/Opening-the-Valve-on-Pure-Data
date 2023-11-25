INPUT=/final_pd_projects_mirrored.txt
while read p; do
    python3 /pd_parsed/sqlite/create_hash_content.py $p
done < $INPUT
