import cv2
import numpy as np


def solve_image(buf: bytes):
    nparr = np.fromstring(buf, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    ret, thresh = cv2.threshold(img_gray, 200, 255, cv2.THRESH_BINARY_INV)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    hierarchy = hierarchy[0]
    for i, c in enumerate(contours):
        ca = cv2.contourArea(c)
        if hierarchy[i][2] < 0 and hierarchy[i][3] < 0:
            if 1700 < ca < 1800:
                M = cv2.moments(c)
                cX = int(M["m10"] / M["m00"]) - 27  # 27 and 34 are the puzzle offsets that are static. i found them by trial and error
                cY = int(M["m01"] / M["m00"]) - 34
                cv2.drawContours(img, contours, i, (0, 0, 255), 1)
                return cX, cY
    return None
