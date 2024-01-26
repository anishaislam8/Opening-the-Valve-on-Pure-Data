INPUT=/branch_name_CORRECT.csv
while read p; do
    python3 create_content_parents_csv.py $p
done < $INPUT
