import os
import cv2
import joblib
import numpy as np
from .. import DIP

path = os.path.dirname(os.path.abspath(__file__))
model = None

def recognize(image) -> str:

    if model is None:
        model = joblib.load(os.path.join(path, 'svm.model'))

    # 转灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 二值化
    # ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    binary = DIP.binarization(gray)

    filtered = DIP.averageFilter(binary, 5)

    # 分割
    images = DIP.split(filtered)
    images = [np.reshape(image, (1, -1)) for image in images]
    return ''.join(model.predict(images))
