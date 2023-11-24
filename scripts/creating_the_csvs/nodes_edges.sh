INPUT=/data/play/aislam4/thesis/final_pd_projects_mirrored.txt
while read p; do
    python3 /data/play/aislam4/thesis/pd_parsed/nodes_edges/nodes_edges.py $p
done < $INPUT
