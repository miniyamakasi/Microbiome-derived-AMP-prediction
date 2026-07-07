#!/usr/bin/env bash
# conda activate MLamp
set -e 

data=$(dirname $PWD);
group=$1;
BIN=/home/Metagenome/LiuQ/ML-AMP/Model
model_path=/home/Metagenome/LiuQ/ML-AMP/Model/best_models
[ ! -d $data/6_Multi/$group ] && mkdir -p $data/6_Multi/$group

for i in `ls $data/5_Binary/$group/*_binary.fasta`;
do
	ID=$(basename $i _binary.fasta);
	python $BIN/predict.py -i $i -p multiple -m $model_path -o $data/6_Multi/$group
done
