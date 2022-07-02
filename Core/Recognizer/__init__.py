import os
import cv2
import joblib
from .. import DIP

path = os.path.dirname(os.path.abspath(__file__))
model = None

def recognize(image) -> str:

    global model
    if model is None:
        model = joblib.load(os.path.join(path, 'svm.model'))

    # 转灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 二值化
    # ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    binary = DIP.binarization(gray)

    # 滤波
    filtered = DIP.averageFilter(binary, 3)

    # 分割
    images = DIP.split(filtered)
    
    # for image in images:
    #     cv2.imshow('image', image)
    #     cv2.waitKey(0)

    images = [image.flatten() for image in images]

    return ''.join(model.predict(images))
