#!/bin/bash
file="pd_blobs.txt"
lines=$(cat $file)
for line in $lines
do
 echo "$line"|~/lookup/getValues b2P|cut -d ";" -f 2- >> pd_projects_new.txt
done