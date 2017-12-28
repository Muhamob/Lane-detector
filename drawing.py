# -*- coding: utf-8 -*-

import numpy as np
import cv2 as cv


def angle(line):
    if line[3] != line[1]:
        return np.abs((line[2] - line[0])/(line[3] - line[1]))
    else: 
        return 99999999

def drawlinesP(image, lines, color, thickness):
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                print(angle(line[0]))
                if angle(line[0]) < 2:
                    cv.line(image, (x1, y1), (x2, y2), color, thickness)
    return image


#def drawmeanP(image, lines, color,thickness):
#    if lines is not None:
        


def drawlines(frame, lines, color, thickness):
    if lines is not None:
        for line in lines:
            for rho, theta in line:
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a*rho
                y0 = b*rho
                x1 = int(x0 + 400*(-b))
                y1 = int(y0 + 400*(a))
                x2 = int(x0 - 400*(-b))
                y2 = int(y0 - 400*(a))
                cv.circle(frame, (int(x0), int(y0)), 3, (255, 0, 0))
                cv.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
    return frame
