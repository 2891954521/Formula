import cv2
import numpy as np


def averageFilter(binary, size) -> np.ndarray:
    '''
    二值图的泛化滤波
    size: 滤波器大小
    '''
    return cv2.filter2D(binary, -1, np.ones((size, size)))


def binarization(image, threshold:int = 63) -> np.ndarray:
    '''
    二值化
    threshold: 切分阈值
    '''
    image = np.array(image, dtype = np.int16)
    image = (image < threshold) * 0 + (threshold < image) * 255
    return 255 - np.array(image, dtype = np.uint8)


def split(binary) -> list:
    '''
    图片分割，沿水平方向分割
    '''
    pos = 0
    images = []

    lines = binary.sum(axis=1)

    while pos < len(lines) - 1:

        start, pos = __findContinuity(lines, pos, len(lines))

        # 找到了一行的底部，切出一整行
        line = binary[start: pos, :]

        cur = 0
        lastWidth = -1
        lastHeight = -1

        row = line.sum(axis=0)

        while cur < len(row) - 1:

            start, cur = __findContinuity(row, cur, len(row))

            if start == -1:
                continue

            # 切出第一个字符
            split = line[:, start: cur]

            start, end = __findBoundary(split.sum(axis=1))

            # 确定切割区域
            split = split[start: end + 1, :]

            width = split.shape[1]
            height = split.shape[0]

            if width > 5 or height > 5:

                if lastHeight != -1 and lastWidth != -1:
                    if  height / lastHeight < 0.4 and width / lastWidth < 0.4:
                        continue
                    
                lastWidth = width
                lastHeight = height

                # 调整为28x28像素
                if width > height:
                    delta = width - height
                    top = delta // 2
                    bottom = delta - top
                    split = cv2.copyMakeBorder(split, top, bottom, 0, 0, cv2.BORDER_CONSTANT, value=0)
                elif width < height:
                    delta = height - width
                    left = delta // 2
                    right = delta - left
                    split = cv2.copyMakeBorder(split, 0, 0, left, right, cv2.BORDER_CONSTANT, value=0)
                split = cv2.resize(split, (28, 28))

                images.append(split)

            start = -1

    return images

    # contours, hierarchy = cv2.findContours(binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # result = []

    # for i in range(len(contours) - 1):
    #     x, y, w, h = cv2.boundingRect(contours[i])
    #     result.append(binary[y:y + h, x:x + w])
    #     # image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 1)
        
    # return result


def __findContinuity(image:np.ndarray, st:int, ed:int) -> tuple:
    '''
    查找连续的区域
    '''
    start = -1
    for i in range(st, ed):

        if image[i] > 0:
            if start == -1:
                start = i
            continue

        if start == -1:
            continue

        return start, i
    return -1, ed


def __findBoundary(col:np.ndarray) -> tuple:
    '''
    查找边界
    '''
    start = -1
    end = -1
    for i in range(len(col)):
        if col[i] > 0:
            start = i
            break
    for i in range(len(col) - 1, -1, -1):
        if col[i] > 0:
            end = i + 1
            break
    return start, end