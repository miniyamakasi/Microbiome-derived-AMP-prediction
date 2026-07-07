#!/usr/bin/env bash
set -e

data=$(dirname $PWD);
group=$1
docker_image=psortb-test
[ ! -d $data/4_PSORT/$group ] && mkdir -p $data/4_PSORT/$group

# docker image create
#docker run -it --name psortb-test \
#	-v /home/Metagenome/LiuQ/Metagenome/SignalP/3_TMHMM:/input \
#	mylab/psortb:3.0.6 \
#	/bin/bash

# length filter 5-50AA
for i in `ls $data/3_TMHMM/$group/*_secreted_seq.fasta`;
do
	seqkit seq -m 5 -M 50 -g $i > ${i%_seq.fasta}_L50.fasta
done

# script prepare
echo -ne "" > $data/temp_bin/${group}_psort.list
for i in `ls $data/3_TMHMM/$group/*_secreted_L50.fasta`;
do
	ID=$(basename $i _secreted_L50.fasta);
	echo "docker exec $docker_image /usr/local/psortb/bin/psort -p /input/$group/${ID}_secreted_L50.fasta -o terse > $data/4_PSORT/$group/${ID}_psort.tab" >> $data/temp_bin/${group}_psort.list
	echo "docker exec $docker_image /usr/local/psortb/bin/psort -n /input/$group/${ID}_secreted_L50.fasta -o terse > $data/4_PSORT/$group/${ID}_psort2.tab" >> $data/temp_bin/${group}_psort.list
done

# ParaFly command
ParaFly -c $data/temp_bin/${group}_psort.list -CPU 10
