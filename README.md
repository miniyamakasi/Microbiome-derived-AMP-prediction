# Microbiome-derived-AMP-prediction
Source code and trained models for microbiome-derived antimicrobial peptide prediction and candidate peptide discovery.

This repository contains the source code and trained models used in the study:

**Hou et al. A microbiome-derived antimicrobial peptide benchmark dataset and candidate peptide resources from colorectal cancer and healthy human gut microbiomes.**

The repository includes:

- Construction of binary and multi-label peptide activity prediction models;
- Secreted peptide screening pipeline for microbiome-derived proteins;
- Trained prediction models;
- Example scripts and datasets for reproducible analyses.

---

# Workflow

## Part I. Model construction

Benchmark AMP datasets
➡
Feature extraction
➡
Binary AMP prediction model
➡
Multi-label activity prediction model
➡
Trained models

## Part II. Candidate peptide discovery

Metagenomic proteins
➡
SignalP 
➡
TMHMM
➡
Length filtering 
➡
PSORTb 
➡
Candidate secreted peptides
➡
Binary AMP prediction
➡
Multi-label activity prediction
➡
Final candidate peptide resources

---

# Repository structure

```text
.
├── Secreted_peptide_analysis/    # Secreted peptide screening pipeline
├── feature_extraction/           # Feature extraction scripts
├── prediction/                   # Model training and prediction scripts
├── best_Model/                   # Trained models
└── example_data/                 # Example input and output files
```

---

# Requirements

- Python >= 3.8
- Biopython
- pandas
- numpy
- scikit-learn
- xgboost
- lightgbm
- catboost
- SignalP 
- TMHMM 
- PSORTb 
- seqkit

Third-party software (SignalP, TMHMM, and PSORTb) should be installed separately according to their official instructions.

---

