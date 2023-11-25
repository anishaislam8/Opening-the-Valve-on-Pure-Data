INPUT=/final_pd_projects_mirrored.txt
while read p; do
    python3 /pd_parsed/nodes_edges/nodes_edges.py $p
done < $INPUT
