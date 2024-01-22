INPUT=/pd_projects_final.txt
while read p; do
    project=`echo $p | sed 's/\_/\//'`
    cd /pd_mirrored
    folder=`echo $p | cut -d\/ -f2`
    mkdir /pd_mirrored/$folder
    mkdir /pd_mirrored_extracted/$folder
    git clone --mirror https://:@github.com/$project /pd_mirrored/$folder
    cd /pd_mirrored/$folder
    branch=`git rev-parse --abbrev-ref HEAD`
    echo $p,$branch >> /pd_parsed/branch_name_CORRECT.csv
    git clone /pd_mirrored/$folder /pd_mirrored_extracted/$folder
done < $INPUT