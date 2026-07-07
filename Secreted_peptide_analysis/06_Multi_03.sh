#!/usr/bin/env bash
# conda activate base
set -e

data=$(dirname $PWD);
group=$1;
#[ ! -d $data/6_Multi/$group ] && mkdir -p $data/6_Multi/$group

for i in `ls $data/6_Multi/$group/*.csv`;
do
	ID=$(basename $i _binary_multi.csv);
	cat $i | sed '1d' | awk -F',' '$3 > 0.5 {print $1}' > $data/6_Multi/$group/${ID}_antibac.ID
	cat $i | sed '1d' | awk -F',' '$4 > 0.5 {print $1}' > $data/6_Multi/$group/${ID}_antifun.ID
	cat $i | sed '1d' | awk -F',' '$5 > 0.5 {print $1}' > $data/6_Multi/$group/${ID}_antican.ID
	cat $i | sed '1d' | awk -F',' '$6 > 0.5 {print $1}' > $data/6_Multi/$group/${ID}_antivir.ID
	seqkit grep -f $data/6_Multi/$group/${ID}_antibac.ID $data/5_Binary/$group/${ID}_binary.fasta -o $data/6_Multi/$group/${ID}_antibac.fasta
	seqkit grep -f $data/6_Multi/$group/${ID}_antifun.ID $data/5_Binary/$group/${ID}_binary.fasta -o $data/6_Multi/$group/${ID}_antifun.fasta
	seqkit grep -f $data/6_Multi/$group/${ID}_antican.ID $data/5_Binary/$group/${ID}_binary.fasta -o $data/6_Multi/$group/${ID}_antican.fasta
	seqkit grep -f $data/6_Multi/$group/${ID}_antivir.ID $data/5_Binary/$group/${ID}_binary.fasta -o $data/6_Multi/$group/${ID}_antivir.fasta
done

