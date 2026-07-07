## binary-classification
### data
import argparse
import os
import pandas as pd
import numpy as np

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, Dense, Flatten, Conv2D, MaxPool2D, LSTM, Dropout
from sklearn.metrics import confusion_matrix, roc_auc_score, matthews_corrcoef
from sklearn.model_selection import StratifiedKFold
from xgboost import XGBClassifier
from utils import get_data_classifier, get_data_classifier_2

def binary_model_kfold(X, y, feature, model_name, kfold, outpath):
    eva_df = pd.DataFrame()
    if model_name == "CNN":
        for fold_idx, (train_idx, test_idx) in enumerate(kfold.split(X, y)):
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
                Dense(1, activation='sigmoid')
            ])
            model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        
            model.fit(train_x.reshape(-1, 50, 20, 1), train_y, batch_size=32, epochs=50)
            pred_proba_y = model.predict(test_x.reshape(-1, 50, 20, 1)).reshape(-1,)
            pred_y = pred_proba_y.round()
            np.savez('%s/evalution/binaryCNN_%s_pred%s.npz'%(outpath, feature, str(fold_idx+1)), y_true=test_y, y_pred=pred_y, y_pred_proba=pred_proba_y)
            temp_eva = evalution_binary(model_name, feature, test_y, pred_y, pred_proba_y)
            eva_df = pd.concat([eva_df, temp_eva], ignore_index=True)

    elif model_name == "LSTM":
        input_dim = X.shape[1]
        for fold_idx, (train_idx, test_idx) in enumerate(kfold.split(X, y)):
            train_x, test_x = X[train_idx], X[test_idx]
            train_y, test_y = y[train_idx], y[test_idx]
            model = Sequential([
                Input(shape=(1, input_dim)),
                LSTM(50,return_sequences=True),
                Dropout(0.1),
                LSTM(50,return_sequences=True),
                Dropout(0.1),
                LSTM(50),
                Dropout(0.1),
                Dense(128),
                Dropout(0.1),
                Dense(1,activation="sigmoid")
            ])
            model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

            if feature == "seq":
                model.fit(train_x.reshape(-1, 1, input_dim), train_y, batch_size=32, epochs=50)
            else:
                model.fit(train_x.reshape(-1, 1, input_dim), train_y, batch_size=128, epochs=50)
            pred_proba_y = model.predict(test_x.reshape(-1, 1, input_dim)).reshape(-1,)
            pred_y = pred_proba_y.round()
            np.savez('%s/evalution/binaryLSTM_%s_pred%s.npz'%(outpath, feature, str(fold_idx+1)), y_true=test_y, y_pred=pred_y, y_pred_proba=pred_proba_y)
            temp_eva = evalution_binary(model_name, feature, test_y, pred_y, pred_proba_y)
            eva_df = pd.concat([eva_df, temp_eva], ignore_index=True)

    elif model_name == "XGBoost":
        for fold_idx, (train_idx, test_idx) in enumerate(kfold.split(X, y)):
            train_x, test_x = X[train_idx], X[test_idx]
            train_y, test_y = y[train_idx], y[test_idx]
            if feature == "seq":
                model = XGBClassifier(learning_rate=0.5, max_depth=6, n_estimators=600,nthread=4,
                                      objective='binary:logistic', use_label_encoder=False)
            elif feature == "phy":
                model = XGBClassifier(learning_rate=0.1, max_depth=6, n_estimators=600,nthread=4,
                                      objective='binary:logistic', use_label_encoder=False)
            model.fit(train_x, train_y)
            pred_y = model.predict(test_x)
            pred_proba_y = model.predict_proba(test_x)[:, 1]
            np.savez('%s/evalution/binaryXGB_%s_pred%s.npz'%(outpath, feature, str(fold_idx+1)), y_true=test_y, y_pred=pred_y, y_pred_proba=pred_proba_y)
            temp_eva = evalution_binary(model_name, feature, test_y, pred_y, pred_proba_y)
            eva_df = pd.concat([eva_df, temp_eva], ignore_index=True)
    
    eva_df['Nkold'] = eva_df.reindex().index
    return eva_df

def evalution_binary(model, feature, y_true, y_pred, y_pred_proba):
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    accuracy = (tp + tn) / (tp + tn + fp + fn)
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    f1 = (2*precision*recall) / (precision + recall)
    auc = roc_auc_score(y_true, y_pred_proba)
    mcc = matthews_corrcoef(y_true, y_pred)
    eva_df = pd.DataFrame({'model': model, 'feature': feature, 'TP': tp, 'FP': fp, 'FN': fn, 'TN': tn, 'Precision': precision,
                           'Recall': recall, 'ACC': accuracy, 'F1': f1, 'AUC': auc, 'MCC': mcc}, index=[0], dtype=object)
    return eva_df

def main():
    parser = argparse.ArgumentParser(description='''
    Usage: python model.py''')
    
    base_path = os.path.dirname(os.path.abspath('.'))
    out_path = os.path.join(base_path, "Model")
    eva_binary_df = pd.DataFrame()
    skfold = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    
    for feature in ['onehot', 'blosum', 'seq', 'phy']:
        if feature == 'onehot' or feature == 'blosum':
            data_path = os.path.join(base_path, "dataset/binary_"+feature+".npz")
            X, y = get_data_classifier_2(data_path)
            eva_df = binary_model_kfold(X, y, feature, "CNN", skfold, out_path)
            eva_binary_df = pd.concat([eva_binary_df, eva_df], ignore_index=True)
        else:
            data_path = os.path.join(base_path, "dataset/binary_"+feature+".csv")
            X, y = get_data_classifier(data_path)
            eva_df1 = binary_model_kfold(X, y, feature, "LSTM", skfold, out_path)
            eva_df2 = binary_model_kfold(X, y, feature, "XGBoost", skfold, out_path)
            eva_binary_df = pd.concat([eva_binary_df, eva_df1], ignore_index=True)
            eva_binary_df = pd.concat([eva_binary_df, eva_df2], ignore_index=True)
            
    eva_binary_df.to_csv(os.path.join(out_path, "eval_binary.csv"))

if __name__ == '__main__':
    main()