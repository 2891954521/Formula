import os
import time
import joblib
from sklearn import svm
from . import DataSet

def SVMTrain():
    st = time.time()

    dataMat, dataLabel = DataSet.loadBinarySplit()

    et = time.time()
    print("Load image spent {:.4f}s.".format((et - st)))
    st = time.time()

    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'svm.model')
    clf = svm.SVC(C = 1.0, kernel='linear', cache_size = 1000, decision_function_shape='ovr')
    rf = clf.fit(dataMat, dataLabel)
    joblib.dump(rf, path)

    et = time.time()
    print("Training spent {:.4f}s.".format((et - st)))
