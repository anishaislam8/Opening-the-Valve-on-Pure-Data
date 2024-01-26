INPUT=../../../csvs/branch_name_CORRECT.csv
while read p; do
    python3 calculate_differences.py $p
done < $INPUT
