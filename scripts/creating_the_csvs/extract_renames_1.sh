INPUT=/data/play/aislam4/thesis/pd_parsed/extraction_parallel/branch_name_1.txt
while read p; do
    folder=`echo $p | cut -d "," -f 1`
    mkdir /data/play/aislam4/thesis/pd_parsed/stats_revisions/$folder
    python3 /data/play/aislam4/thesis/pd_parsed/extract_renames.py $p
done < $INPUT
