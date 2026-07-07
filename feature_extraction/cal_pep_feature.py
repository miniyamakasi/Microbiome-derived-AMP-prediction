import AAComposition, CTD, PseudoAAC, BasicDes
import pandas as pd
import numpy as np

blosum_matrix = np.array([
    [4,  -1, -2, -2, 0,  -1, -1, 0, -2,  -1, -1, -1, -1, -2, -1, 1,  0,  -3, -2, 0],
    [-1, 5,  0,  -2, -3, 1,  0,  -2, 0,  -3, -2, 2,  -1, -3, -2, -1, -1, -3, -2, -3],
    [-2, 0,  6,  1,  -3, 0,  0,  0,  1,  -3, -3, 0,  -2, -3, -2, 1,  0,  -4, -2, -3],
    [-2, -2, 1,  6,  -3, 0,  2,  -1, -1, -3, -4, -1, -3, -3, -1, 0,  -1, -4, -3, -3],
    [0,  -3, -3, -3, 9,  -3, -4, -3, -3, -1, -1, -3, -1, -2, -3, -1, -1, -2, -2, -1],
    [-1, 1,  0,  0,  -3, 5,  2,  -2, 0,  -3, -2, 1,  0,  -3, -1, 0,  -1, -2, -1, -2],
    [-1, 0,  0,  2,  -4, 2,  5,  -2, 0,  -3, -3, 1,  -2, -3, -1, 0,  -1, -3, -2, -2],
    [0,  -2, 0,  -1, -3, -2, -2, 6,  -2, -4, -4, -2, -3, -3, -2, 0,  -2, -2, -3, -3],
    [-2, 0,  1,  -1, -3, 0,  0,  -2, 8,  -3, -3, -1, -2, -1, -2, -1, -2, -2, 2,  -3],
    [-1, -3, -3, -3, -1, -3, -3, -4, -3, 4,  2,  -3, 1,  0,  -3, -2, -1, -3, -1, 3],
    [-1, -2, -3, -4, -1, -2, -3, -4, -3, 2,  4,  -2, 2,  0,  -3, -2, -1, -2, -1, 1],
    [-1, 2,  0,  -1, -3, 1,  1,  -2, -1, -3, -2, 5,  -1, -3, -1, 0,  -1, -3, -2, -2],
    [-1, -1, -2, -3, -1, 0,  -2, -3, -2, 1,  2,  -1, 5,  0,  -2, -1, -1, -1, -1, 1],
    [-2, -3, -3, -3, -2, -3, -3, -3, -1, 0,  0,  -3, 0,  6,  -4, -2, -2, 1,  3,  -1],
    [-1, -2, -2, -1, -3, -1, -1, -2, -2, -3, -3, -1, -2, -4, 7,  -1, -1, -4, -3, -2],
    [1,  -1, 1,  0,  -1, 0,  0,  0,  -1, -2, -2, 0,  -1, -2, -1, 4,  1,  -3, -2, -2],
    [0,  -1, 0,  -1, -1, -1, -1, -2, -2, -1, -1, -1, -1, -2, -1, 1,  5,  -2, -2, 0],
    [-3, -3, -4, -4, -2, -2, -3, -2, -2, -3, -2, -3, -1, 1,  -4, -3, -2, 11, 2,  -3],
    [-2, -2, -2, -3, -2, -1, -2, -3, 2,  -1, -1, -2, -1, 3,  -3, -2, -2, 2,  7,  -1],
    [0,  -3, -3, -3, -1, -2, -2, -3, -3, 3,  1,  -2, 1,  -1, -2, -2, 0,  -3, -1, 4]
])
onehot_matrix = np.eye(20)
mapping = {'A':0, 'R':1, 'N':2, 'D':3, 'C':4, 'Q':5, 'E':6, 'G':7, 'H':8, 'I':9, 'L':10,
           'K':11, 'M':12,'F':13, 'P':14, 'S':15,'T':16, 'W':17, 'Y':18, 'V':19}

"""

"""

def cal_pep_seq(peptides, sequence, type, output_path):
    peptides_descriptors = []
    count = 0

    for peptide in peptides:
        peptides_descriptor = {}
        peptide = str(peptide)
        AAC = AAComposition.CalculateAAComposition(peptide)
        DIP = AAComposition.CalculateDipeptideComposition(peptide)
        peptides_descriptor.update(AAC)
        peptides_descriptor.update(DIP)
        peptides_descriptors.append(peptides_descriptor)

        if count % 100 == 0:
            print("No.%d Peptide: %s" % (count, peptide))
        count += 1
    
    df = pd.DataFrame(peptides_descriptors)
    output_csv = pd.concat([sequence, df, type], axis=1)
    output_csv.to_csv(output_path, encoding="utf8")
    return output_csv

def cal_pep_phy(peptides, sequence, type, output_path):
    peptides_descriptors = []
    count = 0

    for peptide in peptides:
        peptides_descriptor = {}
        peptide = str(peptide)
        CCTD = CTD.CalculateCTD(peptide)
        PAAC = PseudoAAC._GetPseudoAAC(peptide, lamda=5)
        APAAC = PseudoAAC.GetAPseudoAAC(peptide, lamda=5)
        Basic = BasicDes.cal_discriptors(peptide)
        peptides_descriptor.update(CCTD)
        peptides_descriptor.update(PAAC)
        peptides_descriptor.update(APAAC)
        peptides_descriptor.update(Basic)
        peptides_descriptors.append(peptides_descriptor)

        if count % 100 == 0:
            print("No.%d Peptide: %s" % (count, peptide))
        count += 1
        
    df = pd.DataFrame(peptides_descriptors)
    output_csv = pd.concat([sequence, df, type], axis=1)
    output_csv.to_csv(output_path, encoding="utf8")
    return output_csv

def cal_pep_blosum(peptides, type, output_path):
    blosum_descriptors = []
    count = 0

    for peptide in peptides:
        index_seq = [mapping[aa] for aa in str(peptide)]
        blosum_mat = blosum_matrix[index_seq]
        pad_len = 50 - blosum_mat.shape[0]
        blosum_pad = np.pad(blosum_mat, ((pad_len,0),(0,0)), 'constant', constant_values=(0,0))
        blosum_descriptors.append(blosum_pad)

        if count % 100 == 0:
            print("No.%d Peptide: %s" % (count, peptide))
        count += 1

    blosum_df = np.array(blosum_descriptors, dtype=np.float32)
    blosum_type = np.array(type, dtype=np.float32)
    np.savez(output_path, X=blosum_df, y=blosum_type)
    return blosum_df, blosum_type

def cal_pep_onehot(peptides, type, output_path):
    onehot_descriptors = []
    count = 0
    
    for peptide in peptides:
        index_seq = [mapping[aa] for aa in str(peptide)]
        onehot_mat = onehot_matrix[index_seq]
        pad_len = 50 - onehot_mat.shape[0]
        onehot_pad = np.pad(onehot_mat, ((pad_len,0),(0,0)), 'constant', constant_values=(0,0))
        onehot_descriptors.append(onehot_pad)

        if count % 100 == 0:
            print("No.%d Peptide: %s" % (count, peptide))
        count += 1
    
    onehot_df = np.array(onehot_descriptors, dtype=np.float32)
    onehot_type = np.array(type, dtype=np.float32)
    np.savez(output_path, X=onehot_df, y=onehot_type)
    return onehot_df, onehot_type


def cal_predict_binary(peptides, ID):
    peptides_descriptors = []
    count = 0

    for peptide in peptides:
        peptides_descriptor = {}
        peptide = str(peptide)
        CCTD = CTD.CalculateCTD(peptide)
        PAAC = PseudoAAC._GetPseudoAAC(peptide, lamda=5)
        APAAC = PseudoAAC.GetAPseudoAAC(peptide, lamda=5)
        peptides_descriptor.update(CCTD)
        peptides_descriptor.update(PAAC)
        peptides_descriptor.update(APAAC)
        peptides_descriptors.append(peptides_descriptor)

    df = pd.DataFrame(peptides_descriptors)
    output_df = pd.concat([ID, df], axis=1)
    return output_df

def cal_predict_multi(peptides, ID):
    peptides_descriptors = []
    count = 0

    for peptide in peptides:
        peptides_descriptor = {}
        peptide = str(peptide)
        AAC = AAComposition.CalculateAAComposition(peptide)
        DIP = AAComposition.CalculateDipeptideComposition(peptide)
        peptides_descriptor.update(AAC)
        peptides_descriptor.update(DIP)
        peptides_descriptors.append(peptides_descriptor)

    df = pd.DataFrame(peptides_descriptors)
    output_df = pd.concat([ID, df], axis=1)
    return output_df


if __name__ == "__main__":
    file = "./classify_all_sample.csv"
