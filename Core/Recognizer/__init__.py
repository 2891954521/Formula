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

    # 高斯滤波
    blur = cv2.GaussianBlur(gray, (5,5), 0)

    # cv2.imwrite(os.path.join(path, 'blur.png'), blur)

    # 二值化
    ret, binary = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    cv2.imwrite(os.path.join(path, 'binary.png'), binary)

    # 中值滤波
    # filtered = cv2.medianBlur(binary, 3)

    # cv2.imwrite(os.path.join(path, 'filtered.png'), filtered)

    # 分割
    images = DIP.split(binary)
    
    # for image in images:
    #     cv2.imshow('image', image)
    #     cv2.waitKey(0)

    images = [image.flatten() for image in images]

    if len(images) == 0:
        return ''
    else:
        return ''.join(model.predict(images))
