#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="${PROJECT_DIR:-$(cd "$SCRIPT_DIR/.." && pwd)}"
GROUP="${1:?Usage: $0 <group> [project_work_directory]}"
WORK_ROOT="${2:-$PWD}"

PSORT_DIR="$WORK_ROOT/4_PSORT/$GROUP"
TMHMM_DIR="$WORK_ROOT/3_TMHMM/$GROUP"

[[ -d "$PSORT_DIR" ]] || { echo "ERROR: directory not found: $PSORT_DIR" >&2; exit 1; }
[[ -d "$TMHMM_DIR" ]] || { echo "ERROR: directory not found: $TMHMM_DIR" >&2; exit 1; }

shopt -s nullglob
files=("$PSORT_DIR"/*_psort.tab)
(( ${#files[@]} > 0 )) || { echo "ERROR: no *_psort.tab files in $PSORT_DIR" >&2; exit 1; }

for gp_file in "${files[@]}"; do
  name="$(basename "$gp_file" _psort.tab)"
  gn_file="$PSORT_DIR/${name}_psort2.tab"
  fasta_file="$TMHMM_DIR/${name}_secreted_L50.fasta"

  [[ -s "$gn_file" ]] || { echo "ERROR: missing $gn_file" >&2; exit 1; }
  [[ -s "$fasta_file" ]] || { echo "ERROR: missing $fasta_file" >&2; exit 1; }

  awk -F '\t' 'BEGIN{OFS="\t"} NR==1 {print "Sequence_ID","Localization_GramPositive"; next} NF>=2 {print $1,$2}' \
    "$gp_file" > "$PSORT_DIR/${name}_loc.tsv"
  awk -F '\t' 'BEGIN{OFS="\t"} NR==1 {print "Localization_GramNegative"; next} NF>=2 {print $2}' \
    "$gn_file" > "$PSORT_DIR/${name}_loc2.tsv"
  paste "$PSORT_DIR/${name}_loc.tsv" "$PSORT_DIR/${name}_loc2.tsv" \
    > "$PSORT_DIR/${name}_combined_location.tsv"

  Rscript "$SCRIPT_DIR/filter3_lq.r" \
    "$PSORT_DIR/${name}_combined_location.tsv" \
    "$PSORT_DIR/${name}_psort_seq.tab"

  perl "$SCRIPT_DIR/extract_psort_seq_lq.pl" \
    "$PSORT_DIR/${name}_psort_seq.tab" \
    "$fasta_file" \
    "$PSORT_DIR/${name}_psort_seq.fasta"

  rm -f "$PSORT_DIR/${name}_loc.tsv" \
        "$PSORT_DIR/${name}_loc2.tsv" \
        "$PSORT_DIR/${name}_combined_location.tsv"
done

echo "PSORTb filtering completed for group: $GROUP"
