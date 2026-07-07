import os
import joblib

from xgboost import XGBClassifier
from skmultilearn.problem_transform import ClassifierChain
from utils import get_data_classifier, get_data_multiclassifier

def binary_model_save(X, y, outpath):
    model = XGBClassifier(learning_rate=0.1, max_depth=6, n_estimators=600, nthread=4,
                          objective='binary:logistic', use_label_encoder=False)
    model.fit(X, y)
    joblib.dump(model, os.path.join(outpath, 'binary_model.pkl'))

def multi_model_save(X, y, outpath):
    model = XGBClassifier(learning_rate=0.5, max_depth=6, n_estimators=600, nthread=4,
                          objective='binary:logistic', use_label_encoder=False)
    clf = ClassifierChain(model)
    clf.fit(X, y)
    joblib.dump(clf, os.path.join(outpath, 'multi_model.pkl'))


def main():
    base_path = os.path.dirname(os.path.abspath('.'))
    out_path = os.path.join(base_path, "Model/best_models")

    path_phy = os.path.join(base_path, "dataset/binary_phy.csv")
    path_seq = os.path.join(base_path, "dataset/multi_seq.csv")
    X_phy, y_phy = get_data_classifier(path_phy)
    X_seq, y_seq = get_data_multiclassifier(path_seq)
    binary_model_save(X_phy, y_phy, out_path)
    multi_model_save(X_seq, y_seq, out_path)

if __name__ == '__main__':
    main()
