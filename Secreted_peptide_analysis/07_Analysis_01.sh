#!/usr/bin/env bash
# conda activate base
set -e

data=$(dirname $PWD);
group=$1;
[ ! -d $data/7_Analysis/Binary ] && mkdir -p $data/7_Analysis/Binary

for i in `ls $data/5_Binary/$group/*.ID`;
do
	name=$(basename $i _binary.ID);
	sed "s/^/${name}\t/g" $i >> $data/7_Analysis/Binary/${group}_pAMPs.txt
done

:<< EOF
cat metagenome_db.list | while read id;
do
	for i in `ls $data/5_Binary/$id/*.csv`;
	do
		name=$(basename $i _psort_binary.csv);
		cat $i | sed '1d' | cut -d',' -f 1 | sed "s/^/${name}\t/" >> $data/7_Analysis/BSamp_info/${id}.txt;
	done
done
EOF
