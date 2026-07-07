import argparse
import os
from Bio import SeqIO
import pandas as pd
import numpy as np
import joblib
import xgboost as xgb

import sys
sys.path.append("/home/Metagenome/LiuQ/ML-AMP/feature_generator")
import cal_pep_feature
from utils import get_featured_binary, get_featured_multi


def binary_classifier_predict(predict_classifier_file, model_file, outputdir):
    binary_cls_model = joblib.load(model_file)
    sequences, predict_data = get_featured_binary(predict_classifier_file)

    x_pred = predict_data.iloc[:, 1:].values
    y_pred_proba = binary_cls_model.predict_proba(x_pred)
    y_output = y_pred_proba[:, 1].round(3)

    output_name = os.path.splitext(os.path.basename(predict_classifier_file))[0]
    output_result = pd.DataFrame({'sequence': np.array(sequences), 'probability': y_output}, index=predict_data.iloc[:, 0])
    output_file = os.path.join(outputdir, output_name+'_binary.csv')
    output_result.to_csv(output_file, encoding='utf8')

def multi_classifier_predict(predict_classifier_file, model_file, outputdir):
    multi_cls_model = joblib.load(model_file)
    sequences, predict_data = get_featured_multi(predict_classifier_file)

    x_pred = predict_data.iloc[:, 1:].values
    y_pred_proba = multi_cls_model.predict_proba(x_pred)
    y_output = y_pred_proba.A.round(3)
    y_output = pd.DataFrame(y_output, columns=['antibacterial', 'antifungal', 'anticancer', 'antiviral'])

    output_name = os.path.splitext(os.path.basename(predict_classifier_file))[0]
    output_result = pd.concat([sequences, y_output], axis=1).set_index(predict_data.iloc[:, 0])
    output_file = os.path.join(outputdir, output_name+'_multi.csv')
    output_result.to_csv(output_file, encoding='utf8')

def total_classifier_predict(predict_classifier_file, binary_file, multi_file, outputdir):
    binary_cls_model = joblib.load(binary_file)
    multi_cls_model = joblib.load(multi_file)
    sequences, predict_binary = get_featured_binary(predict_classifier_file)
    
    ## binary classification
    x_pred = predict_binary.iloc[:, 1:].values
    y_pred = binary_cls_model.predict_proba(x_pred).argmax(axis=1)
    ## get predictive AMP items and feature
    binary_seq = sequences[y_pred == 1].values.copy().tolist()
    binary_id = predict_binary.iloc[:, 0][y_pred == 1]
    if not binary_seq:
        print("fasta file did not predict the AMP.")
    else:
        predict_multi = cal_pep_feature.cal_predict_multi(binary_seq, binary_id)
        ## multiple classification
        x_pred_multi = predict_multi.iloc[:, 1:].values
        y_pred_multi = multi_cls_model.predict_proba(x_pred_multi)
        y_output = y_pred_multi.A.round(3)
        y_output = pd.DataFrame(y_output, columns=['antibacterial', 'antifungal', 'anticancer', 'antiviral'])

        output_name = os.path.splitext(os.path.basename(predict_classifier_file))[0]
        output_result = pd.concat([sequences, y_output], axis=1).set_index(binary_id)
        output_file = os.path.join(outputdir, output_name+'_total.csv')
        output_result.to_csv(output_file, encoding='utf8')

def is_fasta(filename):
    try:
        records = list(SeqIO.parse(filename, "fasta"))
        return len(records) > 0
    except Exception as e:
        return False

def main():
    parser = argparse.ArgumentParser(description='''
    Usage:python predict.py -i /path/to/predict.fasta -p binary -m Model/best_models -o output_dir''')
    parser.add_argument('-i', dest="input_fasta", help="Input predict fasta file")
    parser.add_argument('-p', dest="pattern", help="Predictive pattern(binary/multiple/total)")
    parser.add_argument('-m', dest="model_path", help="Model pkl path")
    parser.add_argument('-o', dest="output_path", help="Output path")
    args = parser.parse_args()
    print(args)

    predict_fasta = args.input_fasta
    pattern = args.pattern
    output_path = args.output_path
    model_path = args.model_path
    model_binary = os.path.join(model_path, 'binary_model.pkl')
    model_multi = os.path.join(model_path, 'multi_model.pkl')

    if not os.path.exists(output_path):
        os.makedirs(output_path)
    if not is_fasta(predict_fasta):
        print('Input is not in fasta format. Please try again.')
    else:
        if pattern == 'binary':
            binary_classifier_predict(predict_fasta, model_binary, output_path)
        elif pattern == 'multiple':
            multi_classifier_predict(predict_fasta, model_multi, output_path)
        elif pattern == 'total':
            total_classifier_predict(predict_fasta, model_binary, model_multi, output_path)

if __name__ == '__main__':
    main()
