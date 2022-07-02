import os
import cv2

from Core import DIP

def loadData() -> tuple:
    path = os.path.dirname(os.path.abspath(__file__))

    image = cv2.imread(os.path.join(path, 'Data/data.png'))

    # 转灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 二值化
    binary = DIP.binarization(gray, 160)

    # cv2.imwrite(os.path.join(path, 'Data/binary.png'), binary)

    # 分割
    images = DIP.split(binary)
    
    # 处理为一维
    images = [image.flatten() for image in images]

    char = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '/', '-', '*']
    labels = [[i] * 60 for i in char]

    return images, labels