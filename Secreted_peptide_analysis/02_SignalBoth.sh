#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORK_DIR="${1:-$PWD}"

cd "$WORK_DIR"

GP_SUMMARY="SignalPredResult_summary.signalp5"
GN_SUMMARY="SignalPredResult2_summary.signalp5"
PROTEIN_FASTA="protein.fasta"

for f in "$GP_SUMMARY" "$GN_SUMMARY" "$PROTEIN_FASTA"; do
  [[ -s "$f" ]] || { echo "ERROR: missing or empty file: $WORK_DIR/$f" >&2; exit 1; }
done

awk -F '\t' '!/^#/ && NF >= 2 {print $1}' "$GP_SUMMARY" > query.txt
awk -F '\t' '!/^#/ && NF >= 2 {print $2}' "$GP_SUMMARY" > Gram_positive.txt
awk -F '\t' '!/^#/ && NF >= 2 {print $2}' "$GN_SUMMARY" > Gram_negative.txt
paste query.txt Gram_positive.txt Gram_negative.txt > filter.txt

Rscript "$SCRIPT_DIR/filter.r" filter.txt type.txt
perl "$SCRIPT_DIR/extract_type_seq.pl" \
  type.txt "$PROTEIN_FASTA" signal_cut.fasta "$GP_SUMMARY" "$GN_SUMMARY"

rm -f query.txt Gram_positive.txt Gram_negative.txt filter.txt type.txt

echo "SignalP consensus filtering completed: $WORK_DIR/signal_cut.fasta"
