INPUT=../../../csvs/branch_name_CORRECT.csv
while read p; do
    python3 extract_revisions.py $p
done < $INPUT
