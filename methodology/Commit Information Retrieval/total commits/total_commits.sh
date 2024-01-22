INPUT=/final_pd_projects_mirrored.txt
while read p; do
    cd /pd_mirrored_extracted/$p
    size=`git --no-pager log --all --pretty=tformat:"%H %P" | wc -l`
    echo $p,$size >> /pd_parsed/project_size/total_commits.txt
done < $INPUT