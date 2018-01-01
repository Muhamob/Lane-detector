# -*- coding: utf-8 -*-

import numpy as np
import cv2 as cv


def angle(line):
    if line[3] != line[1]:
        return np.abs((line[2] - line[0])/(line[3] - line[1]))
    else:
        return 99999999


def drawlinesP(image, lines, color, thickness=3):
    maxangle = 2
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                print(angle(line[0]))
                if angle(line[0]) < maxangle:
                    cv.line(image, (x1, y1), (x2, y2), color, thickness)
    return image


def fillLane(leftLine, rightLine, frame, color=(255, 102, 153), brightness=.8):
    if leftLine is not None and rightLine is not None:
        if len(leftLine) != 0 and len(rightLine) != 0:
            p1 = [leftLine[0][0][0], leftLine[0][0][1]]
            p2 = [leftLine[0][0][2], leftLine[0][0][3]]
            p3 = [rightLine[0][0][2], rightLine[0][0][3]]
            p4 = [rightLine[0][0][0], rightLine[0][0][1]]
            zero = np.zeros_like(frame)
            cv.fillPoly(zero, np.array([[p1, p2, p3, p4]], dtype=np.int32), color)
            drawlinesP(zero, leftLine, (51, 51, 204))
            drawlinesP(zero, rightLine, (51, 51, 204))
            return cv.addWeighted(frame, 1.0, zero, brightness, 0.0)
    else:
        print('nf fillLane')
        return frame
