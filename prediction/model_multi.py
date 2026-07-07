import argparse
import os
import pandas as pd
import numpy as np

# from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, Dense, Flatten, Conv2D, MaxPool2D, LSTM, Dropout
from sklearn.metrics import hamming_loss, label_ranking_loss, accuracy_score, precision_score, average_precision_score, recall_score, f1_score, roc_auc_score
from sklearn.model_selection import StratifiedKFold
from xgboost import XGBClassifier
from skmultilearn.problem_transform import ClassifierChain
from utils import get_data_multiclassifier, get_data_classifier_2

def multi_model_kfold(X, y, feature, model_name, kfold, outpath):
    eva_df = pd.DataFrame()
    y_stratify = y.sum(axis=1)
    if model_name == "CNN":
        for fold_idx, (train_idx, test_idx) in enumerate(kfold.split(X, y_stratify)):
            train_x, test_x = X[train_idx], X[test_idx]
            train_y, test_y = y[train_idx], y[test_idx]
            model = Sequential([
                Input(shape=(50, 20, 1)),
                Conv2D(32, kernel_size=(3, 3), activation='relu'),
                MaxPool2D(pool_size=(2, 2)),
                Conv2D(64, kernel_size=(3, 3), activation='relu'),
                MaxPool2D(pool_size=(2, 2)),
                Flatten(),
                Dense(128, activation='relu'),
                Dense(4, activation='sigmoid')
            ])
            model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

            model.fit(train_x.reshape(-1, 50, 20, 1), train_y, batch_size=32, epochs=10)
            pred_proba_y = model.predict(test_x.reshape(-1, 50, 20, 1))
            pred_y = pred_proba_y.round()
            np.savez('%s/evalution/multiCNN_%s_pred%s.npz'%(outpath, feature, str(fold_idx+1)), y_true=test_y, y_pred=pred_y, y_pred_proba=pred_proba_y)
            temp_eva = evalution_multiple(model_name, feature, test_y, pred_y, pred_proba_y)
            eva_df = pd.concat([eva_df, temp_eva], ignore_index=True)

    elif model_name == "LSTM":
        input_dim = X.shape[1]
        for fold_idx, (train_idx, test_idx) in enumerate(kfold.split(X, y_stratify)):
            train_x, test_x = X[train_idx], X[test_idx]
            train_y, test_y = y[train_idx], y[test_idx]
            model = Sequential([
                Input(shape=(1, input_dim)),
                LSTM(50, return_sequences=True),
                Dropout(0.1),
                LSTM(50, return_sequences=True),
                Dropout(0.1),
                LSTM(50),
                Dropout(0.1),
                Dense(128),
                Dropout(0.1),
                Dense(4, activation='sigmoid')
            ])
            model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

            model.fit(train_x.reshape(-1, 1, input_dim), train_y, batch_size=32, epochs=10)
            pred_proba_y = model.predict(test_x.reshape(-1, 1, input_dim))
            pred_y = pred_proba_y.round()
            np.savez('%s/evalution/multiLSTM_%s_pred%s.npz'%(outpath, feature, str(fold_idx+1)), y_true=test_y, y_pred=pred_y, y_pred_proba=pred_proba_y)
            temp_eva = evalution_multiple(model_name, feature, test_y, pred_y, pred_proba_y)
            eva_df = pd.concat([eva_df, temp_eva], ignore_index=True)

    elif model_name == "XGBoost":
        for fold_idx, (train_idx, test_idx) in enumerate(kfold.split(X, y_stratify)):
            train_x, test_x = X[train_idx], X[test_idx]
            train_y, test_y = y[train_idx], y[test_idx]
            if feature == 'seq':
                model = XGBClassifier(learning_rate=0.5, max_depth=6, n_estimators=600,
                                      nthread=4, objective='binary:logistic', use_label_encoder=False)
            else:
                model = XGBClassifier(learning_rate=0.1, max_depth=6, n_estimators=600,
                                      nthread=4, objective='binary:logistic', use_label_encoder=False)
            clf = ClassifierChain(model)

            clf.fit(train_x, train_y)
            pred_y = clf.predict(test_x).A
            pred_proba_y = clf.predict_proba(test_x).A
            np.savez('%s/evalution/multiXGB_%s_pred%s.npz'%(outpath, feature, str(fold_idx+1)), y_true=test_y, y_pred=pred_y, y_pred_proba=pred_proba_y)
            temp_eva = evalution_multiple(model_name, feature, test_y, pred_y, pred_proba_y)
            eva_df = pd.concat([eva_df, temp_eva], ignore_index=True)
        
    eva_df['Nfold'] = eva_df.reindex().index
    return eva_df

def evalution_multiple(model, feature, y_true, y_pred, y_pred_proba):
    hl = hamming_loss(y_true, y_pred)
    rl = label_ranking_loss(y_true, y_pred)
    oe = one_error(y_true, y_pred)
    cov = Coverage(y_true, y_pred)
    subset_acc = accuracy_score(y_true, y_pred)
    microP, macroP = precision_score(y_true, y_pred, average='micro'), precision_score(y_true, y_pred, average='macro')
    averageP = average_precision_score(y_true, y_pred)
    microR, macroR = recall_score(y_true, y_pred, average='micro'), recall_score(y_true, y_pred, average='macro')
    microF1, macroF1 = f1_score(y_true, y_pred, average='micro'), f1_score(y_true, y_pred, average='macro')
    Acc = Accuracy(y_true, y_pred)
    auc, macro_auc = roc_auc_score(y_true, y_pred_proba), roc_auc_score(y_true, y_pred_proba, average='macro')

    eva_multi_df = pd.DataFrame({'model':model, 'feature':feature, 'hamming_loss':hl, 'ranking_loss':rl, 'one_error':oe, 
                                 'coverage':cov, 'subset_acc':subset_acc, 'microP':microP, 'macroP':macroP, 'averageP':averageP,
                                 'microR':microR, 'macroR':macroR, 'microF1':microF1, 'macroF1':macroF1, 'Accuracy':Acc, 'auc':auc,
                                 'macroAUC':macro_auc}, index=[0], dtype=object)
    return eva_multi_df

def Accuracy(y_true, y_pred):
    count = 0
    for i in range(y_true.shape[0]):
        p = sum(np.logical_and(y_true[i], y_pred[i]))
        q = sum(np.logical_or(y_true[i], y_pred[i]))
        count += p / q
    return count / y_true.shape[0]

def one_error(y_true, y_pred):
    max_indices = np.argmax(y_pred, axis=1)
    one_errors = [1 if y_true[i][idx] == 0 else 0 for i, idx in enumerate(max_indices)]
    return np.mean(one_errors)

def Coverage(y_true, y_pred):
    ranks = np.argsort(-np.array(y_pred), axis=1)  # 按降序排列索引
    coverage = []
    for i, true_labels in enumerate(y_true):
        relevant_ranks = [list(ranks[i]).index(j) + 1 for j, is_relevant in enumerate(true_labels) if is_relevant]
        coverage.append(max(relevant_ranks))
    return np.mean(coverage)

def main():
    parser = argparse.ArgumentParser(description='''
    Usage: python model_multi.py''')

    base_path = os.path.dirname(os.path.abspath('.'))
    out_path = os.path.join(base_path, "Model")
    eva_multi_df = pd.DataFrame()
    skfold = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    for feature in ['blosum', 'seq', 'phy']:
        if feature == 'blosum':
            data_path = os.path.join(base_path, "dataset/multi_"+feature+".npz")
            X, y = get_data_classifier_2(data_path)
            
            eva_df = multi_model_kfold(X, y, feature, "CNN", skfold, out_path)
            eva_multi_df = pd.concat([eva_multi_df, eva_df], ignore_index=True)
        elif feature == 'seq':
            data_path = os.path.join(base_path, "dataset/multi_"+feature+".csv")
            X, y = get_data_multiclassifier(data_path)
            eva_df1 = multi_model_kfold(X, y, feature, "LSTM", skfold, out_path)
            eva_df2 = multi_model_kfold(X, y, feature, "XGBoost", skfold, out_path)
            eva_multi_df = pd.concat([eva_multi_df, eva_df1], ignore_index=True)
            eva_multi_df = pd.concat([eva_multi_df, eva_df2], ignore_index=True)
        else:
            data_path = os.path.join(base_path, "dataset/multi_"+feature+".csv")
            X, y = get_data_multiclassifier(data_path)
            eva_df = multi_model_kfold(X, y, feature, "XGBoost", skfold, out_path)
            eva_multi_df = pd.concat([eva_multi_df, eva_df], ignore_index=True)
    
    eva_multi_df.to_csv(os.path.join(out_path, "eval_multiple.csv"))

if __name__ == '__main__':
    main()