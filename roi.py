# -*- coding: utf-8 -*-

import numpy as np
import cv2 as cv
# import matplotlib.pyplot as plt


def applyMask(frame, mask):
    """
    Uses to apply given mask to frame
    input : frame - image, numpy array
            mask - mask, 255 true 0 false
    output : frame_out - np array like frame where everything instead mask
             is black
    """
    return np.bitwise_and(frame, mask)


def mask(points, shape=[720, 360], dtype=np.uint8, frame=None):
    """
    Create the mask by the given method
    input : points - vertices of polygon
            shape - shape of image where we apply mask
            dtype - dtype of frame, uint8 is default
    output : np array with given shape and dtype
            255 - True, 0 - False
    NOTE!!!
    array of vertices should be like this
    np.array([[[10, 10], [40, 45], [10, 40]]], dtype=np.int32)
    ALSO!!!
    x and y are from top left corner
    """
    if frame is None:
        mask = np.zeros(shape=shape, dtype=dtype)
    else:
        mask = np.zeros_like(frame)
    if len(shape) == 2:
        cv.fillPoly(mask, points, 255)
    else:
        cv.fillPoly(mask, points, (255,)*shape[2])
    return mask
