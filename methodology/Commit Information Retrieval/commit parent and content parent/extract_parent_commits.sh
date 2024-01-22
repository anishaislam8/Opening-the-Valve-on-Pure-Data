INPUT=project_name.txt
while read p; do
    cd /pd_mirrored_extracted/$p
    git --no-pager log --all --pretty=tformat:"%H %P" > /pd_parsed/parents/$p.txt
done < $INPUT
