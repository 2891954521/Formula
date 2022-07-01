import cv2

from . import DIP
from .. import Tool

def recognize(image) -> str:

    # 转灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 二值化
    # ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    binary = DIP.binarization(gray)

    # 分割
    images = DIP.split(binary)
    
    # Tool.ShowImage(result)

    return ''