import pandas as pd

for pos in ['gut','oral','skin','vagina']:
    df = pd.read_csv(pos+'_cdhit_multi.csv')
    antibac_seq, antifun_seq, antican_seq, antivir_seq = [], [], [], []
    for index, row in df.iterrows():
        if row['antibacterial'] > 0.5:
            antibac_seq.append(f">{row['ID']}\n{row['sequence']}")
        elif row['antifungal'] > 0.5:
            antifun_seq.append(f">{row['ID']}\n{row['sequence']}")
        elif row['antiviral'] > 0.5:
            antivir_seq.append(f">{row['ID']}\n{row['sequence']}")
	elif row['anticancer'] > 0.5:
            antican_seq.append(f">{row['ID']}\n{row['sequence']}")
    with open(pos+'_antibac.fasta', 'w') as f:
        for seq in antibac_seq:
            f.write(seq+'\n')
    with open(pos+'_antifun.fasta', 'w') as f:
        for seq in antifun_seq:
            f.write(seq+'\n')
    with open(pos+'_antican.fasta', 'w') as f:
        for seq in antican_seq:
            f.write(seq+'\n')
    with open(pos+'_antivir.fasta', 'w') as f:
        for seq in antivir_seq:
            f.write(seq+'\n')
