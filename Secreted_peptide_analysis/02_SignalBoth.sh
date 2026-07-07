grep -v "^#" SignalPredResult_summary.signalp5 | awk -F '\t' '{print $1}' > query.txt
grep -v "^#" SignalPredResult_summary.signalp5 | awk -F '\t' '{print $2}' > Gram+.txt
grep -v "^#" SignalPredResult2_summary.signalp5 | awk -F '\t' '{print $2}' > Gram-.txt 
paste query.txt Gram+.txt Gram-.txt > filter.txt
Rscript filter.r
rm *.txt
perl extract_type_seq.pl
mv signal_cut.fasta ../seq
mv *.signalp5 ../seq
mv *.tab ../seq
