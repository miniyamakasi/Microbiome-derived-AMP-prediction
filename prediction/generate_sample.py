import pandas as pd
import numpy as np
import cal_pep_feature
from Bio import SeqIO
import os


class GenerateSample():
    def __init__(self, positive_fasta, negative_fasta, generate_file_path):
        self.positive_fasta = positive_fasta
        self.negative_fasta = negative_fasta
        self.generate_file_path = generate_file_path

    def __call__(self, *args, **kwargs):
        positive_sample = self.generate_peptides(self.positive_fasta)
        negative_sample = self.generate_peptides(self.negative_fasta)
        all_sample = self.concat_datasets(positive_sample, negative_sample)
        # Generate classifier sample
        print("generating classify sample......")

        sequence = all_sample["sequence"]
        peptides = sequence.values.copy().tolist()
        type = all_sample["type"]
        # output_path = os.path.join(self.generate_file_path, "classify_sample.csv")
        output_seq = os.path.join(self.generate_file_path, "binary_seq.csv")
        output_phy = os.path.join(self.generate_file_path, "binary_phy.csv")
        output_onehot = os.path.join(self.generate_file_path, "binary_onehot.npz")
        output_blosum = os.path.join(self.generate_file_path, "binary_blosum.npz")
        df_seq = cal_pep_feature.cal_pep_seq(peptides, sequence, type, output_seq)
        df_phy = cal_pep_feature.cal_pep_phy(peptides, sequence, type, output_phy)
        onehot_df, onehot_type = cal_pep_feature.cal_pep_onehot(peptides, type, output_onehot)
        blosum_df, blosum_type = cal_pep_feature.cal_pep_blosum(peptides, type, output_blosum)

        print("split train/test sample......")
        self.split_sample(df_seq, "binary_seq")
        self.split_sample(df_phy, "binary_phy")
        self.split_sample_2(onehot_df, onehot_type, "binary_onehot")
        self.split_sample_2(blosum_df, blosum_type, "binary_blosum")
        print("split sample is ok!")

    def generate_peptides(self, fasta_file):
        data_all = [[], []]
        for record in SeqIO.parse(fasta_file, "fasta"):
            data_all[0].append(str(record.seq))
            if 'Positive' in record.id:
                data_all[1].append(1)
            else:
                data_all[1].append(0)
        data_all = list(map(list, zip(*data_all)))
        data = pd.DataFrame(data=data_all, columns=["sequence", "type"])
        return data

    def concat_datasets(self, positive_file, negative_file):
        data_concat = pd.concat([positive_file, negative_file], ignore_index=True, axis=0)
        data_concat = data_concat.sample(frac=1, random_state=None)
        data_concat.reset_index(drop=True, inplace=True)
        return data_concat

    def split_sample(self, generate_all_df, feature):
        num = generate_all_df.shape[0]
        train_sample = generate_all_df.iloc[:int(0.85 * num), :]
        test_sample = generate_all_df.iloc[int(0.85 * num):, :]
        train_sample.to_csv(os.path.join(self.generate_file_path, feature+"_train.csv"), encoding="utf8", index=False)
        test_sample.to_csv(os.path.join(self.generate_file_path, feature+"_test.csv"), encoding="utf8", index=False)
    
    def split_sample_2(self, generate_all_df, generate_all_type, feature):
        num = generate_all_df.shape[0]
        train_sample, train_type = generate_all_df[:int(0.85 * num)], generate_all_type[:int(0.85 * num)]
        test_sample, test_type = generate_all_df[int(0.85 * num):], generate_all_type[int(0.85 * num):]
        np.savez(os.path.join(self.generate_file_path, feature+"_train.npz"), X=train_sample, y=train_type)
        np.savez(os.path.join(self.generate_file_path, feature+"_test.npz"), X=test_sample, y=test_type)

if __name__ == "__main__":
    """
    positive_path = "path_to_positive_fasta_file"
    negative_path = "path_to_negative_fasta_file"
    generate_file_path = "path_to_save_splited_files"
    """
    base_path = os.path.dirname(os.path.abspath('.'))
    positive_path = os.path.join(base_path, "dataset", "pos.fasta")
    negative_path = os.path.join(base_path, "dataset", "neg.fasta")
    generate_file_path = os.path.join(base_path, "dataset")
    GenerateSample(positive_path, negative_path, generate_file_path)()
