import os
import time
import joblib
from sklearn import svm
from . import DataSet

def SVMTrain():
    st = time.time()
    dataMat, dataLabel = DataSet.loadData()
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'svm.model')
    clf = svm.SVC(C=1.0, kernel='rbf', decision_function_shape='ovr')
    rf = clf.fit(dataMat, dataLabel)
    joblib.dump(rf, path)
    et = time.time()
    print("Training spent {:.4f}s.".format((et - st)))
