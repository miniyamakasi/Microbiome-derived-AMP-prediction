#!/usr/bin/env bash
# conda activate MLamp
set -e 

data=$(dirname $PWD);
group=$1;
BIN=/home/Metagenome/LiuQ/ML-AMP/Model
model_path=/home/Metagenome/LiuQ/ML-AMP/Model/best_models
[ ! -d $data/5_Binary/$group ] && mkdir -p $data/5_Binary/$group

for i in `ls $data/4_PSORT/$group/*_psort_seq.fasta`;
do
	ID=$(basename $i _psort_seq.fasta);
	seqkit grep -v -s -r -p "[^ARNDCQEGHILKMFPSTWYV]" $i > $data/4_PSORT/$group/${ID}_psort.fasta
done

find $data/4_PSORT/$group -size 0c | xargs rm -f

for i in `ls $data/4_PSORT/$group/*_psort.fasta`;
do
	ID=$(basename $i _psort.fasta);
	python $BIN/predict.py -i $i -p binary -m $model_path -o $data/5_Binary/$group
done
