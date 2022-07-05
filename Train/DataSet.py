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


def createBinary():
    '''
    将原图转为二值图
    '''
    path = os.path.dirname(os.path.abspath(__file__))

    images = os.listdir(os.path.join(path, 'Data/resurces'))

    for image in images:
        img = cv2.imread(os.path.join(path, 'Data/resurces/' + image))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        binary = DIP.binarization(gray, 135)
        filtered = cv2.medianBlur(binary, 3)
        filtered = DIP.averageFilter(filtered, 3)
        cv2.imwrite(os.path.join(path, 'Data/binary/' + image.split('.')[0] + '.png'), filtered)


def binarySplit(files: list = None):
    '''
    将binary下的二值图分割为单个字符
    files: 指定需要分割的图片
    '''
    path = os.path.dirname(os.path.abspath(__file__))

    if files is None:
        images = os.listdir(os.path.join(path, 'Data/binary'))
    else:
        images = files

    for image in images:
        img = cv2.imread(os.path.join(path, 'Data/binary/' + image))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        retval, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        file = os.path.join(path, 'Data/split/' + image.split('.')[0].split('_')[0])
        if not os.path.exists(file):
            os.mkdir(file)
        outs = DIP.split(binary)
        count = len(os.listdir(file))
        for i in range(len(outs)):
            cv2.imwrite(os.path.join(file, str(i + count) + '.png'), outs[i])


def loadBinarySplit() -> tuple:
    '''
    将二值图读入
    '''

    images = []
    labels = []

    path = os.path.dirname(os.path.abspath(__file__))

    chars = os.listdir(os.path.join(path, 'Data/split'))
    ch = None
    for char in chars:

        if char == 'x':
            ch = '*'
        elif char == 'V':
            ch = '/'
        else:
            ch = char

        images_ = os.listdir(os.path.join(path, 'Data/split/' + char))
        for image in images_:
            img = cv2.imread(os.path.join(path, 'Data/split/' + char + '/' + image), cv2.IMREAD_GRAYSCALE)
            images.append(img.flatten())
            labels.append(ch)

    return images, labels
