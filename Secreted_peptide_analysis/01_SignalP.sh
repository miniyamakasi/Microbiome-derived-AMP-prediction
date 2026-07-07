#prepare file .fasta,must protein
#-batch for Number of sequences that the tool will run simultaneously.(default 10000)
#-org for Organism. Archaea: 'arch', Gram-positive: 'gram+', Gram-negative: 'gram-' or Eukarya: 'euk' (default "euk")
#-format :Output format. 'long' for generating the predictions with plots, 'short' for the predictions without plots.
#-prefix :Output files prefix. (default "Input file prefix")
#-mature :Make fasta file with mature sequence for predictingt transmembrane regions

DB=/home/Metagenome/LiuQ/Metagenome/Pep-Seq

signalp -fasta $DB/AMR/*.fa -batch 300000 \
	-org gram+ \
	-format short \
	-prefix  SignalPredResult \
	-mature

signalp -fasta $DB/AMR/*.fa -batch 2000 \
       	-org gram- \
      	-format short \
     	-prefix  SignalPredResult2 \
	-mature

