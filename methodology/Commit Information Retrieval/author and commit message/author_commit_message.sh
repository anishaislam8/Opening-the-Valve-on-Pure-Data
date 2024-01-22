INPUT=branch_name_CORRECT.csv
IFS=','
while read -r p br; do
    folder=`echo $p | cut -d\/ -f2`
    cd /pd_mirrored_extracted/$folder
    git checkout $br
    git --no-pager log --all --pretty=tformat:"%H" > /pd_parsed/author_commit_message/commits.txt
    INPUT2=/pd_parsed/author_commit_message/commits.txt
    while read k; do
        author=`git show -s --format="%an_COMMA_%ae_COMMA_%cn_COMMA_%ce" $k`
        commit_message=`git show -s --format=%B $k`
        echo $p,$k,$author >> /pd_parsed/author_commit_message/author.csv
        echo $p,$k,$commit_message >> /pd_parsed/author_commit_message/commit_message.csv
    done < $INPUT2
    rm /pd_parsed/author_commit_message/commits.txt
done < $INPUT
