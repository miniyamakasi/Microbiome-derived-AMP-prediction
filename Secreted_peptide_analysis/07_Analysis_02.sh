#!/usr/bin/env bash
# conda activate MLamp
set -e

data=$(dirname $PWD);

cat $data/bin/RA.list | while read id;
do
	python $data/bin/taxnomy_info_merge.py $data/7_Analysis/Binary/${id}_pAMPs.txt $data/7_Analysis/reads-assign/$id/${id}.genus.type.list.txt
	python $data/bin/taxnomy_info_merge.py $data/7_Analysis/Binary/${id}_pAMPs.txt $data/7_Analysis/reads-assign/$id/${id}.phylum.type.list.txt
	python $data/bin/taxnomy_info_merge.py $data/7_Analysis/Binary/${id}_pAMPs.txt $data/7_Analysis/reads-assign/$id/${id}.species.type.list.txt
done

:<< EOF
cat $data/bin/RA.list | while read id;
do
	python $data/bin/taxnomy_info_merge.py $data/7_Analysis/BSamp_info/${id}.txt $data/7_Analysis/reads-assign/$id/${id}.genus.type.list.txt
done
EOF
