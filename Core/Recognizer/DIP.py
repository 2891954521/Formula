import cv2
import numpy as np


def binarization(image, threshold:int = 127) -> np.ndarray:
    '''
    二值化
    threshold: 切分阈值
    '''
    image = np.array(image, dtype = np.int16)
    image = (image < threshold) * 0 + (threshold < image) * 255
    return np.array(image, dtype = np.uint8)


def split(binary) -> list:
    '''
    图片分割
    '''
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    result = []

    for i in range(len(contours) - 1):
        x, y, w, h = cv2.boundingRect(contours[i])
        result.append(binary[y:y + h, x:x + w])
        # image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 1)
        
    return result
