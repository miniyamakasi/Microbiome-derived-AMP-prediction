#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
GROUP="${1:?Usage: $0 <group> [project_work_directory]}"
WORK_ROOT="${2:-$PWD}"

PREDICT_SCRIPT="$REPO_DIR/prediction/predict.py"
MODEL_DIR="$REPO_DIR/best_Model"
INPUT_DIR="$WORK_ROOT/5_Binary/$GROUP"
OUTPUT_DIR="$WORK_ROOT/6_Multi/$GROUP"
mkdir -p "$OUTPUT_DIR"

[[ -f "$PREDICT_SCRIPT" ]] || { echo "ERROR: missing $PREDICT_SCRIPT" >&2; exit 1; }
[[ -d "$MODEL_DIR" ]] || { echo "ERROR: missing $MODEL_DIR" >&2; exit 1; }

shopt -s nullglob
files=("$INPUT_DIR"/*_binary.fasta)
(( ${#files[@]} > 0 )) || { echo "ERROR: no *_binary.fasta files in $INPUT_DIR" >&2; exit 1; }

for fasta in "${files[@]}"; do
  python "$PREDICT_SCRIPT" -i "$fasta" -p multiple -m "$MODEL_DIR" -o "$OUTPUT_DIR"
done
