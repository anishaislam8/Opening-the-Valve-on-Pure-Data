INPUT=/data/play/aislam4/thesis/pd_parsed/extraction_parallel/project_name1.txt
while read p; do
    python3 /data/play/aislam4/thesis/pd_parsed/create_new_csv_to_store_hashes/create_csv_for_hash_ids_1.py $p
done < $INPUT
