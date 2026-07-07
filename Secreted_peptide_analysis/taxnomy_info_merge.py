#!/usr/bin/env python
# coding: utf-8

import sys
import pandas as pd
import os

pIDs_path = sys.argv[1]
taxinfo_path = sys.argv[2]

# loadFile
pIDs = pd.read_csv(pIDs_path, sep='\t', header=None)
pIDs.columns = ['sample','gene']
taxinfo = pd.read_csv(taxinfo_path,sep='\t',header=None)
taxinfo.columns = ['sample','tax','gene']

# match taxonomy info
taxpAMP = {'sample':[], 'gene':[], 'tax':[]}
for sample in pIDs['sample'].unique():
    geneIDs = pIDs['gene'][pIDs['sample']==sample]
    df_sample = taxinfo[taxinfo['sample']==sample]
    for gene in geneIDs:
        tax = df_sample['tax'][df_sample['gene'].str.contains(gene+'\D')]
        taxpAMP['sample'].append(sample)
        taxpAMP['gene'].append(gene)
        if tax.empty:
            taxpAMP['tax'].append(None)
        else:
            taxpAMP['tax'].append(tax.values[0])

# output
filepath = os.path.split(pIDs_path)[0]
filename = os.path.splitext(os.path.basename(pIDs_path))[0]
extension = os.path.basename(taxinfo_path).split('.')[1]
outpath = os.path.join(filepath, filename+'.'+extension+'.txt')

pd.DataFrame(taxpAMP).to_csv(outpath)

