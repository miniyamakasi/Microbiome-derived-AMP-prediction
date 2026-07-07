import pandas as pd
import numpy as np
import cal_pep_feature
from Bio import SeqIO
import time
import os

class GenerateMultiSample():
    def __init__(self, antibac_fasta, antifun_fasta, antican_fasta, antivir_fasta, generate_file_path):
        self.antibac_fasta = antibac_fasta
        self.antifungal_fasta = antifun_fasta
        self.anticancer_fasta = antican_fasta
        self.antiviral_fasta = antivir_fasta
        self.generate_file_path = generate_file_path

    def __call__(self, *args, **kwargs):
        class_sample = self.generate_peptides(self.antibac_fasta, self.antifungal_fasta, self.anticancer_fasta, self.antiviral_fasta)
        # Generate multi-classifier sample
        print("generating multi-classify sample......")

        sequence = class_sample["sequence"]
        peptides = sequence.values.copy().tolist()
        type = class_sample.iloc[:, 1:]
        # output_path = os.path.join(self.generate_file_path, type[0] + "_sample.csv")
        output_seq = os.path.join(self.generate_file_path, "multi_seq.csv")
        output_phy = os.path.join(self.generate_file_path, "multi_phy.csv")
        output_onehot = os.path.join(self.generate_file_path, "multi_onehot.npz")
        output_blosum = os.path.join(self.generate_file_path, "multi_blosum.npz")
        df_seq = cal_pep_feature.cal_pep_seq(peptides, sequence, type, output_seq)
        df_phy = cal_pep_feature.cal_pep_phy(peptides, sequence, type, output_phy)
        onehot_df, onehot_type = cal_pep_feature.cal_pep_onehot(peptides, type, output_onehot)
        blosum_df, blosum_type = cal_pep_feature.cal_pep_blosum(peptides, type, output_blosum)

        print("split train/test sample......")
        self.split_sample(df_seq, "multi_seq")
        self.split_sample(df_phy, "multi_phy")
        self.split_sample_2(onehot_df, onehot_type, "multi_onehot")
        self.split_sample_2(blosum_df, blosum_type, "multi_blosum")
        print("split sample is ok!")

    def generate_peptides(self, antibac_fasta, antifungal_fasta, anticancer_fasta, antiviral_fasta):
        antibac_seq = [str(record.seq) for record in SeqIO.parse(antibac_fasta, "fasta")]
        antifun_seq = [str(record.seq) for record in SeqIO.parse(antifungal_fasta, "fasta")]
        antican_seq = [str(record.seq) for record in SeqIO.parse(anticancer_fasta, "fasta")]
        antivir_seq = [str(record.seq) for record in SeqIO.parse(antiviral_fasta, "fasta")]

        class_sequence = list(set(antibac_seq + antifun_seq + antican_seq + antivir_seq))
        num = len(class_sequence)
        data_all = {'sequence': class_sequence, 'antibacterial': np.zeros(num, dtype=int), 'antifungal': np.zeros(num, dtype=int),
                    'anticancer': np.zeros(num, dtype=int), 'antiviral': np.zeros(num, dtype=int)}
        for seq in antibac_seq:
            pos = data_all['sequence'].index(seq)
            data_all['antibacterial'][pos] = 1
        for seq in antifun_seq:
            pos = data_all['sequence'].index(seq)
            data_all['antifungal'][pos] = 1
        for seq in antican_seq:
            pos = data_all['sequence'].index(seq)
            data_all['anticancer'][pos] = 1
        for seq in antivir_seq:
            pos = data_all['sequence'].index(seq)
            data_all['antiviral'][pos] = 1
        data = pd.DataFrame(data_all)

        return data
    
    def split_sample(self, generate_class_df, feature):
        num = generate_class_df.shape[0]
        train_sample = generate_class_df.iloc[:int(0.85 * num), :]
        test_sample = generate_class_df.iloc[int(0.85 * num):, :]
        train_sample.to_csv(os.path.join(self.generate_file_path, feature+"_train.csv"), encoding="utf8", index=False)
        test_sample.to_csv(os.path.join(self.generate_file_path, feature+"_test.csv"), encoding="utf8", index=False)

    def split_sample_2(self, generate_class_df, generate_class_type, feature):
        num = generate_class_df.shape[0]
        train_sample, train_type = generate_class_df[:int(0.85 * num)], generate_class_type[:int(0.85 * num)]
        test_sample, test_type = generate_class_df[int(0.85 * num):], generate_class_type[int(0.85 * num):]
        np.savez(os.path.join(self.generate_file_path, feature+"_train.npz"), X=train_sample, y=train_type)
        np.savez(os.path.join(self.generate_file_path, feature+"_test.npz"), X=test_sample, y=test_type)


if __name__ == "__main__":
    base_path = os.path.dirname(os.path.abspath('.'))
    antibac_path = os.path.join(base_path, "dataset", "antibacterial.fasta")
    antifungal_path = os.path.join(base_path, "dataset", "antifungal.fasta")
    anticancer_path = os.path.join(base_path, "dataset", "anticancer.fasta")
    antiviral_path = os.path.join(base_path, "dataset", "antiviral.fasta")
    generate_file_path = os.path.join(base_path, "dataset")

    GenerateMultiSample(antibac_path, antifungal_path, anticancer_path, antiviral_path, generate_file_path)()