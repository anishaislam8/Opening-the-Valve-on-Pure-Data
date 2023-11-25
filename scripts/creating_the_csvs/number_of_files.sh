INPUT=/final_pd_projects_mirrored.txt
while read p; do
    cd /pd_parsed/stats_revisions/$p
    total_files=`ls | wc -l`
    unique_files=`ls | awk -F '_CMMT_' '{print $1}' | sort -u | wc -l`
    echo $p,$total_files,$unique_files >> /pd_parsed/csvs/number_of_files_per_project.csv
done < $INPUT
