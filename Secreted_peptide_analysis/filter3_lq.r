#!/usr/bin/env Rscript

# Combine Gram-positive and Gram-negative PSORTb results and retain sequences
# that are not assigned to intracellular compartments by either model.
#
# Usage:
#   Rscript filter3_lq.r <combined_location.tsv> <selected_ids.tsv>
#
# Input columns:
#   Sequence_ID  Localization_GramPositive  Localization_GramNegative
#
# By default, Cytoplasmic and CytoplasmicMembrane/InnerMembrane predictions
# are treated as intracellular. Unknown predictions are retained because they
# do not provide evidence of intracellular localization. This script is a
# conservative computational filter, not experimental proof of secretion.

args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 2L) {
  stop("Usage: Rscript filter3_lq.r <combined_location.tsv> <selected_ids.tsv>",
       call. = FALSE)
}

input_file <- args[1]
output_file <- args[2]

if (!file.exists(input_file)) {
  stop("Input file does not exist: ", input_file, call. = FALSE)
}

x <- read.delim(
  input_file,
  header = TRUE,
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
colnames(x) <- c("Sequence_ID", "Localization_GramPositive", "Localization_GramNegative")

normalize_location <- function(z) {
  z <- trimws(as.character(z))
  z[is.na(z)] <- ""
  # Remove punctuation/spaces to tolerate PSORTb label variants.
  tolower(gsub("[^[:alnum:]]", "", z))
}

# PSORTb commonly reports Cytoplasmic and CytoplasmicMembrane. InnerMembrane
# and PlasmaMembrane are included as defensive aliases for alternate outputs.
intracellular_labels <- c(
  "cytoplasmic",
  "cytoplasm",
  "cytoplasmicmembrane",
  "innermembrane",
  "plasmamembrane"
)

loc_gp <- normalize_location(x$Localization_GramPositive)
loc_gn <- normalize_location(x$Localization_GramNegative)

intracellular_gp <- loc_gp %in% intracellular_labels
intracellular_gn <- loc_gn %in% intracellular_labels
keep <- nzchar(trimws(x$Sequence_ID)) & !intracellular_gp & !intracellular_gn

out <- x[keep, , drop = FALSE]
write.table(
  out,
  file = output_file,
  sep = "\t",
  quote = FALSE,
  row.names = FALSE,
  col.names = TRUE
)

message("Retained ", nrow(out), " of ", nrow(x),
        " sequences not assigned to an intracellular compartment by either PSORTb model.")
