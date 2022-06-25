import cv2
import threading
import numpy as np

from . import Analyzer
from . import Recognizer

analyzer = Analyzer
recognizer = Recognizer


class testShow(threading.Thread):

    def __init__(self, image):
        super().__init__()
        self.image = image
    
    def run(self):
        cv2.imshow("test", self.image)
        cv2.waitKey()


def process(file) -> str:
    # 将获取到的字符流数据转换成1维数组
    data = np.frombuffer(file, np.uint8)
    # 将数组解码成图像
    image = cv2.imdecode(data, cv2.IMREAD_COLOR)

    # testShow(image).start()

    result = recognizer.recognize(image)
    
    return analyzer.analyze(result)
