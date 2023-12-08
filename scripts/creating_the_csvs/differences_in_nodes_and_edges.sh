INPUT=/branch_name_CORRECT.csv
while read p; do
    python3 differences_in_nodes_and_edges.py $p
done < $INPUT
