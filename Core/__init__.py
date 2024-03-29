import cv2
import numpy as np

from .Analyzer import FourArithmetic

from . import Recognizer

recognizer = Recognizer

def process(bytes) -> tuple:
    # 将获取到的字符流数据转换成1维数组
    data = np.frombuffer(bytes, np.uint8)
    # 将数组解码成图像
    image = cv2.imdecode(data, cv2.IMREAD_COLOR)

    formula = recognizer.recognize(image)
    
    return (formula, FourArithmetic().analyze(formula))
