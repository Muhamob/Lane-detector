import numpy as np
import cv2 as cv


def angle(line):
    if line[3] != line[1]:
        return np.abs((line[2] - line[0])/(line[3] - line[1]))
    else:
        return 99999999


def drawlinesP(image, lines, color, thickness):
    maxangle = 2
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                print(angle(line[0]))
                if angle(line[0]) < maxangle:
                    cv.line(image, (x1, y1), (x2, y2), color, thickness)
    return image
