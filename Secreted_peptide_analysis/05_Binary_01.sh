#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
GROUP="${1:?Usage: $0 <group> [project_work_directory]}"
WORK_ROOT="${2:-$PWD}"

PREDICT_SCRIPT="$REPO_DIR/prediction/predict.py"
MODEL_DIR="$REPO_DIR/best_Model"
INPUT_DIR="$WORK_ROOT/4_PSORT/$GROUP"
OUTPUT_DIR="$WORK_ROOT/5_Binary/$GROUP"
mkdir -p "$OUTPUT_DIR"

[[ -f "$PREDICT_SCRIPT" ]] || { echo "ERROR: missing $PREDICT_SCRIPT" >&2; exit 1; }
[[ -d "$MODEL_DIR" ]] || { echo "ERROR: missing $MODEL_DIR" >&2; exit 1; }

shopt -s nullglob
files=("$INPUT_DIR"/*_psort_seq.fasta)
(( ${#files[@]} > 0 )) || { echo "ERROR: no *_psort_seq.fasta files in $INPUT_DIR" >&2; exit 1; }

for fasta in "${files[@]}"; do
  id="$(basename "$fasta" _psort_seq.fasta)"
  clean_fasta="$INPUT_DIR/${id}_psort.fasta"
  seqkit grep -v -s -r -p '[^ARNDCQEGHILKMFPSTWYV]' "$fasta" > "$clean_fasta"
  [[ -s "$clean_fasta" ]] || { echo "WARNING: no canonical sequences retained for $id" >&2; rm -f "$clean_fasta"; continue; }
  python "$PREDICT_SCRIPT" -i "$clean_fasta" -p binary -m "$MODEL_DIR" -o "$OUTPUT_DIR"
done
