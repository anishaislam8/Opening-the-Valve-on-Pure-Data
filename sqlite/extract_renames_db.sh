INPUT=csvs/branch_name_CORRECT.csv
while read p; do
    python3 extract_renames_db.py $p
done < $INPUT
