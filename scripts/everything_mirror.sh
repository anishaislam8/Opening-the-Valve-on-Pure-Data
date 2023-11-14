INPUT=/data/play/aislam4/thesis/final_final_pd_projects.txt
while read p; do
    project=`echo $p | sed 's/\_/\//'`
    cd /data/play/aislam4/thesis/pd_mirrored
    folder=`echo $p | cut -d\/ -f2`
    mkdir /data/play/aislam4/thesis/pd_mirrored/$folder
    mkdir /data/play/aislam4/thesis/pd_mirrored_extracted/$folder
    git clone --mirror https://:@github.com/$project /data/play/aislam4/thesis/pd_mirrored/$folder
    cd /data/play/aislam4/thesis/pd_mirrored/$folder
    branch=`git rev-parse --abbrev-ref HEAD`
    echo $p,$branch >> /data/play/aislam4/thesis/pd_parsed/branch_name_MIRROR.txt
    git clone /data/play/aislam4/thesis/pd_mirrored/$folder /data/play/aislam4/thesis/pd_mirrored_extracted/$folder
done < $INPUT