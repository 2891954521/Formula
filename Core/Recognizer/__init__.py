import os
import cv2
import joblib
import numpy as np
from .. import DIP

path = os.path.dirname(os.path.abspath(__file__))

tmpPath = os.path.join(path, 'test')
if not os.path.exists(tmpPath):
    os.mkdir(tmpPath)

model = None

def recognize(image) -> str:

    global model
    if model is None:
        model = joblib.load(os.path.join(path, 'svm.model'))

    # 转灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 高斯滤波
    blur = cv2.GaussianBlur(gray, (5,5), 0)

    # cv2.imwrite(os.path.join(path, 'test/blur.png'), blur)

    # 二值化
    ret, binary = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    cv2.imwrite(os.path.join(path, 'test/binary.png'), binary)

    # 中值滤波
    # filtered = cv2.medianBlur(binary, 3)

    # cv2.imwrite(os.path.join(path, 'filtered.png'), filtered)

    # 分割
    lines = DIP.splitByLine(binary)
    
    # for image in images:
    #     cv2.imshow('image', image)
    #     cv2.waitKey(0)

    count  = 0
    result = ''
    for line in lines:

        if len(line) == 0:
            continue

        count += 1
        preview = np.zeros((28, 30 * len(line)), dtype = np.uint8)

        for i in range(len(line)):
            preview[ : , i * 30 + 1: i * 30 + 29] = line[i]

        cv2.imwrite(os.path.join(path, 'test/preview_' + str(count) + '.png'), preview)
        
        images = [image.flatten() for image in line]
        
        result += ''.join(model.predict(images)) + '\n'

    return result
