import sys
sys.path.append("/home/Metagenome/LiuQ/ML-AMP/feature_generator")
import cal_pep_feature

from Bio import SeqIO
import pandas as pd
import numpy as np

def get_data_classifier(all_data_path):
    data = pd.read_csv(all_data_path, encoding="utf8", index_col=0)
    X = data.iloc[:, 1:-1].values
    y = data.iloc[:, -1].values
    return X, y

def get_data_classifier_2(all_data_path):
    data = np.load(all_data_path)
    X, y = data["X"], data["y"]
    return X, y

def get_data_multiclassifier(all_data_path):
    data = pd.read_csv(all_data_path, encoding="utf8", index_col=0)
    X = data.iloc[:, 1:-4].values
    y = data.iloc[:, -4:].values
    return X, y

def get_featured_binary(fasta_file_path):
    data_all = [[],[]]
    for record in SeqIO.parse(fasta_file_path, "fasta"):
        data_all[0].append(record.id)
        data_all[1].append(str(record.seq))
    data_all = list(map(list, zip(*data_all)))
    data = pd.DataFrame(data=data_all, columns=["ID", "sequence"])

    sequence = data["sequence"]
    peptides = sequence.values.copy().tolist()
    ID = data["ID"]
    predict_featured_data = cal_pep_feature.cal_predict_binary(peptides, ID)

    return sequence, predict_featured_data

def get_featured_multi(fasta_file_path):
    data_all = [[], []]
    for record in SeqIO.parse(fasta_file_path, "fasta"):
        data_all[0].append(record.id)
        data_all[1].append(str(record.seq))
    data_all = list(map(list, zip(*data_all)))
    data = pd.DataFrame(data=data_all, columns=["ID", "sequence"])

    sequence = data["sequence"]
    peptides = sequence.values.copy().tolist()
    ID = data["ID"]
    predict_featured_data = cal_pep_feature.cal_predict_multi(peptides, ID)

    return sequence, predict_featured_data

