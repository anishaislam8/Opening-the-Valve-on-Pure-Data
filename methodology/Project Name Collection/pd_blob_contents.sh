INPUT=pd_blobs.txt
while read p; do
    cd pd_blobs_new
    echo "$p"|~/lookup/showCnt blob 1|cut -d\; -f 2|base64 -d >> $p.txt
    cd ../
done < $INPUT