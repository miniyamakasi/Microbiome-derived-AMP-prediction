#!/usr/bin/env bash
set -e

data=$(dirname $PWD);
group=$1;

cd $data/4_PSORT/$group;
for i in `ls $data/4_PSORT/$group/*_psort.tab`;
do
	name=$(basename $i _psort.tab);
	cat $i | cut -f 1,2 > ${name}_loc.txt
	cat ${i%.tab}2.tab | cut -f 2 | sed '1c Localization2' > ${name}_loc2.txt
	paste ${name}_loc.txt ${name}_loc2.txt > ${name}_filter3.txt
	Rscript $data/bin/filter3_lq.r ./${name}_filter3.txt ./${name}_psort_seq.tab
	perl $data/bin/extract_psort_seq_lq.pl ./${name}_psort_seq.tab $data/3_TMHMM/$group/${name}_secreted_L50.fasta ./${name}_psort_seq.fasta
	rm *.txt
done
