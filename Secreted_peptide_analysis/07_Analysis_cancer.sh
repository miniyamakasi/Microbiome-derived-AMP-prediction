#!/usr/bin/env bash
# conda activate base
set -e

data=$(dirname $PWD);
group=$1;
[ ! -d $data/7_Analysis/Multi ] && mkdir -p $data/7_Analysis/Multi

for i in `ls $data/6_Multi/$group/*.csv`;
do
	name=$(basename $i _binary_multi.csv);
	cat $i | sed '1d' | awk -F',' '$5 > 0.5 {print $1}' | sed "s/^/${name}\t/g" >> $data/7_Analysis/Multi/${group}_pAntican.txt
done
