INPUT=/pd_parsed/extraction_parallel/branch_name_1.txt
while read p; do
    python3 /pd_parsed/nodes_edges/difference_in_nodes_edges_1.py $p
done < $INPUT
