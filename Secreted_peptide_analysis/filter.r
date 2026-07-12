#!/usr/bin/env Rscript

# Select sequences predicted to contain a signal peptide by at least one
# SignalP organism model (Gram-positive or Gram-negative).
#
# Usage:
#   Rscript filter.r filter.txt type.txt
#
# Input filter.txt: three tab-separated columns without a header:
#   sequence_id  gram_positive_prediction  gram_negative_prediction
# SignalP 5 predictions such as OTHER, SP(Sec/SPI), LIPO(Sec/SPII),
# TAT(Tat/SPI), and TATLIPO(Tat/SPII) are supported.

args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1L || length(args) > 2L) {
  stop("Usage: Rscript filter.r <filter.txt> [type.txt]", call. = FALSE)
}

input_file <- args[1]
output_file <- if (length(args) == 2L) args[2] else "type.txt"

if (!file.exists(input_file)) {
  stop("Input file does not exist: ", input_file, call. = FALSE)
}

x <- read.delim(
  input_file,
  header = FALSE,
  sep = "\t",
  quote = "",
  comment.char = "",
  stringsAsFactors = FALSE,
  fill = TRUE,
  check.names = FALSE
)

if (ncol(x) < 3L) {
  stop("Input must contain at least three tab-separated columns.", call. = FALSE)
}

x <- x[, 1:3, drop = FALSE]
colnames(x) <- c("Sequence_ID", "Gram_positive", "Gram_negative")

clean_prediction <- function(z) {
  z <- trimws(as.character(z))
  z[is.na(z)] <- ""
  toupper(z)
}

is_signal <- function(z) {
  z <- clean_prediction(z)
  nzchar(z) & !(z %in% c("OTHER", "NO_SP", "NONE", "NA", "N/A", "UNKNOWN"))
}

keep_gp <- is_signal(x$Gram_positive)
keep_gn <- is_signal(x$Gram_negative)
keep <- nzchar(trimws(x$Sequence_ID)) & (keep_gp | keep_gn)

out <- x[keep, , drop = FALSE]
out$Selected_model <- ifelse(
  keep_gp[keep] & keep_gn[keep], "both",
  ifelse(keep_gp[keep], "gram_positive", "gram_negative")
)

# The legacy Perl script requires the sequence identifier in the first column.
write.table(
  out,
  file = output_file,
  sep = "\t",
  quote = FALSE,
  row.names = FALSE,
  col.names = FALSE
)

message("Retained ", nrow(out), " of ", nrow(x),
        " sequences with a signal-peptide prediction.")
