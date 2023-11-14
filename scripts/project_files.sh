INPUT=/data/play/aislam4/thesis/downloaded_pd_projects.txt
while read p; do
    cd /data/play/aislam4/thesis/pd_projects/$p
    branch=`git rev-parse --abbrev-ref HEAD`
    git ls-tree -r --name-only $branch >> /data/play/aislam4/thesis/pd_git_files/$p.txt
    cd /data/play/aislam4/thesis
done < $INPUT