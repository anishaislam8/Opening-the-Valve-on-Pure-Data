INPUT=/data/play/aislam4/thesis/test.txt
while read p; do
    python3 /data/play/aislam4/thesis/pd_parsed/sqlite/create_hash_content.py $p
done < $INPUT
