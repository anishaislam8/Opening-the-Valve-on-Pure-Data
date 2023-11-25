INPUT=/pd_parsed/extraction_parallel/branch_name_1.txt
IFS=','
while read -r p br; do
    folder=`echo $p | cut -d\/ -f2`
    ls /pd_parsed/stats_revisions/$folder | sed 's/\.[^.]*$//' | awk -F '_CMMT_' '{print $2}'> /pd_parsed/author_commit_message/commits_1.txt
    cd /pd_mirrored_extracted/$folder
    git checkout $br
    INPUT2=/pd_parsed/author_commit_message/commits_1.txt
    while read k; do
        author=`git show -s --format="%an_COMMA_%ae_COMMA_%cn_COMMA_%ce" $k`
        commit_message=`git show -s --format=%B $k`
        echo $p,$k,$author >> /pd_parsed/author_commit_message/author_1.csv
        echo $p,$k,$commit_message >> /pd_parsed/author_commit_message/commit_message_1.csv
    done < $INPUT2
    rm /pd_parsed/author_commit_message/commits_1.txt
done < $INPUT
