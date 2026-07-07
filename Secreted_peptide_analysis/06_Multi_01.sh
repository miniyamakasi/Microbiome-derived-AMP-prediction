#!/usr/bin/env bash
# conda activate base
set -e

data=$(dirname $PWD);
group=$1;
[ ! -d $data/6_Multi/$group ] && mkdir -p $data/6_Multi/$group

for i in `ls $data/5_Binary/$group/*.csv`;
do
	ID=$(basename $i _psort_binary.csv);
	cat $i | sed '1d' | awk -F',' '$3 > 0.5 {print $1}' > $data/5_Binary/$group/${ID}_binary.ID
	seqkit grep -f $data/5_Binary/$group/${ID}_binary.ID $data/4_PSORT/$group/${ID}_psort.fasta -o $data/5_Binary/$group/${ID}_binary.fasta
done

