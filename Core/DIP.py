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
    row = binary.sum(axis=0)

    start = -1
    
    images = []

    for i in range(len(row)):

        if row[i] > 0:
            if start == -1:
                # 确定左边界
                start = i
        elif start != -1:
            # 确定 右边界 和 切割区域
            split = binary[:, start: i]
            col = split.sum(axis=1)
            start = -1
            end = -1
            for j in range(len(col)):
                if col[j] > 0:
                    start = j
                    break
            for j in range(len(col) - 1, -1, -1):
                if col[j] > 0:
                    # 确定下边界
                    end = j
                    break
            # 确定切割区域
            split = split[start: end, :]
            if split.shape[1] > 5 and split.shape[0] > 5:
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
