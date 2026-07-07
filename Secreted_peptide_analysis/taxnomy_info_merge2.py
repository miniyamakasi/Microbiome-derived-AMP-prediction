#!/usr/bin/env python
# coding: utf-8

import sys
import pandas as pd
import re
import os

ID_path = sys.argv[1]
tax_path = sys.argv[2]

# loadFile
df_ID = pd.read_csv(ID_path, sep='\t', header=None)
df_ID.columns = ['sample','gene']
df_tax = pd.read_csv(tax_path, sep='\t')
df_tax.columns = ['Gene_ID','tax']

# match taxonomy info
if 'PRJEB36291' in ID_path:
    df_ID['Gene_ID'] = df_ID['sample']+'.fastq.gz_'+df_ID['gene']
elif 'VMRC' in ID_path:
    df_ID['Gene_ID'] = df_ID['sample']+'_'+df_ID['gene']

df_merge = pd.merge(df_ID,df_tax,how='left')
df_merge['tax'][df_merge['tax'].notnull()] = [re.sub(r'\s+\[[A-Z]\]\s+','',string) for string in df_merge['tax'][df_merge['tax'].notnull()]]

# output
filepath = os.path.split(ID_path)[0]
filename = os.path.splitext(os.path.basename(ID_path))[0]
extension = os.path.basename(tax_path).split('.')[5].replace('Reads2','').lower()
outpath = os.path.join(filepath, filename+'.'+extension+'.txt')

df_merge.loc[:, ['sample','gene','tax']].to_csv(outpath)

