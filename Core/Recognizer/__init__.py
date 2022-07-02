import cv2

from .. import DIP, Tool

def recognize(image) -> str:

    # 转灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 二值化
    # ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    binary = DIP.binarization(gray)

    filtered = DIP.averageFilter(binary, 5)

    cv2.imwrite(f'/test/test.jpg', filtered)

    # 分割
    images = DIP.split(filtered)
    
    for i in range(len(images)):
        cv2.imshow(f'{i}', images[i])
        # cv2.imwrite(f'{i}.jpg', images[i])
    cv2.waitKey()

    return ''