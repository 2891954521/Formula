import os
import cv2
import numpy as np
from Core import DIP

def loadData() -> tuple:
    path = os.path.dirname(os.path.abspath(__file__))

    image = cv2.imread(os.path.join(path, 'Data/data.png'))

    # 转灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 二值化
    binary = DIP.binarization(gray, 160)

    # cv2.imwrite(os.path.join(path, 'Data/binary.png'), binary)

    # 分割为28x28像素的字符
    images = DIP.split(binary)

    # 处理为一维
    images = [image.flatten() for image in images]
    # np.reshape(image, (1, -1))
    char = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '/', '-', '*']
    labels = [ch for ch in char for i in range(60)]

    return images, labels