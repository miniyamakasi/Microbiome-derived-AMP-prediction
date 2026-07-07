#!/usr/bin/env bash
# TMHMM v2.0 filtering
# Retain sequences with PredHel=0

for i in *.fasta
do
    name=$(basename $i .fasta)

    tmhmm $i > ${name}_tmhmm.txt

    grep "PredHel=0" ${name}_tmhmm.txt | cut -f1 > ${name}.id

    seqkit grep -f ${name}.id $i > ${name}_secreted_seq.fasta
done