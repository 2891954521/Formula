import os
import cv2

def loadData() -> list:
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Data')
    print(path)
    names = os.listdir(path)
    print(names)
    result = []
    for name in names:
        image = cv2.imread(os.path.join(path, name))
        width = image.shape[1] // 12
        height = image.shape[0] // 5
        images = []
        for y in range(0, image.shape[0], height):
            for x in range(0, image.shape[1], width):
                images.append(image[y:y+height, x:x+width])
        result.append((name.split('.')[0].replace('x', '*').replace('I','/'), images))
    return result