import cv2
import threading

class ShowImage(threading.Thread):

    def __init__(self, image):
        super().__init__()
        self.image = image
        self.start()


    def run(self):
        cv2.imshow("image", self.image)
        cv2.waitKey()
