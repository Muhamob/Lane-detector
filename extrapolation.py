import numpy as np
import cv2 as cv


def getSlope(line):
        p1p2 = np.array([line[0][2], line[0][3]]) - np.array(
                [line[0][0], line[0][1]])  # p2 - p1

        if p1p2[0] == 0:
            return 9999999
        else:
            return p1p2[1]/p1p2[0]


def separateLines(lines):
    """
    Implementation of separating lines by its slope
    left line has negative slope
    right line has positive slope
    """
    left_line = []
    right_line = []
    if lines is not None:
        for line in lines:
            if getSlope(line) < 0:
                left_line.append(line)
            else:
                right_line.append(line)
    return left_line, right_line


def make_line_points(y1, y2, line):
    """
    Convert a line represented in slope and intercept into pixel points
    """
    if line is None:
        return None
    print(line)
    slope, intercept = line

    # make sure everything is integer as cv2.line requires it
    x1 = int((y1 - intercept)/slope)
    x2 = int((y2 - intercept)/slope)
    y1 = int(y1)
    y2 = int(y2)

    return ((x1, y1), (x2, y2))


def lane_lines(image, lines):
    left_lane, right_lane = separateLines(lines)

    y1 = image.shape[0]  # bottom of the image
    y2 = y1*0.6         # slightly lower than the middle

    left_line = make_line_points(y1, y2, left_lane)
    right_line = make_line_points(y1, y2, right_lane)

    return left_line, right_line


def draw_lane_lines(image, lines, color=[255, 0, 0], thickness=20):
    # make a separate image to draw lines and combine with the orignal later
    line_image = np.zeros_like(image)
    for line in lines:
        if line is not None:
            cv.line(line_image, *line,  color, thickness)
    # image1 * α + image2 * β + λ
    # image1 and image2 must be the same shape.
    return cv.addWeighted(image, 1.0, line_image, 0.95, 0.0)
