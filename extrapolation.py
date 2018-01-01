import numpy as np
import cv2 as cv


def getSlope(line):
    """
    Returns tan = delta y div delta x
    NOTE y goes down and x goes right from
    top left corner
    """
    p1p2 = np.array([line[0][2], line[0][3]]) - np.array(
            [line[0][0], line[0][1]])  # p2 - p1
    if p1p2[0] == 0:
        return 9999999
    else:
        return p1p2[1]/p1p2[0]


def getLength(line):
    """
    Returns euclidean norm of line
    line is a sequence of start point and end point
    e.g. [[0, 0, 1, 1]] = [[x1, y1, x2, y2]]
    """
    return np.sqrt((line[0][0]-line[0][2])**2 + (line[0][1] - line[0][3])**2)


def separateLines(lines):
    """
    Implementation of separating lines by its slope
    left line has negative slope
    right line has positive slope
    """
    left_line = []
    right_line = []
    if lines is not None and len(lines) != 0:
        for line in lines:
            if getSlope(line) < 0:
                left_line.append(line)
            else:
                right_line.append(line)
        print('checked separateLines')
    else:
        print('nf separate')
    print(len(left_line), len(right_line))
    return left_line, right_line


def averageLines(lines):
    """
    Returns mean of slopes and max of lengths
    for given lines
    """
    meanSlope = 0
    maxLength = 0
    if lines is not None and len(lines) != 0:
        slopes = np.array([getSlope(line) for line in lines])
        lengths = np.array([getLength(line) for line in lines])
        meanSlope = slopes.mean()
        maxLength = lengths.max()
    return meanSlope, maxLength


def lstsqLine(lines, bottomLevel=244, topLevel=190):
    """
    Fit line between given points (x1, y1) and (x2, y2)
    that are combined together
    return: - line from min(x) to max(x), where
            x is an array of abscissa
            - None if lines is None
    """
    if lines is not None and len(lines) != 0:
        x = np.array([line[0][0] for line in lines] +
                      [line[0][2] for line in lines])
        y = np.array([line[0][1] for line in lines] +
                      [line[0][3] for line in lines])

        A = np.vstack([x, np.ones(len(x))]).T
        a, c = np.linalg.lstsq(A, y)[0]
        Ax = np.vstack([y, np.ones(len(y))]).T
        b, d = np.linalg.lstsq(Ax, x)[0]  # x = b + d*y
        x0 = int((bottomLevel - c)/a) if a != 0 else int(b + d*bottomLevel)
        x1 = int((topLevel - c)/a) if a != 0 else int(b + d*topLevel)
        return [[[x0, int(c+a*x0), x1, int(c+a*x1)]]]
    else:
        return None


def draw_lane_lines(image, lines, color=[255, 0, 0], thickness=20):
    """
    not my implementation, will be removed soon
    """
    # make a separate image to draw lines and combine with the orignal later
    line_image = np.zeros_like(image)
    for line in lines:
        if line is not None:
            cv.line(line_image, *line,  color, thickness)
    # image1 * α + image2 * β + λ
    # image1 and image2 must be the same shape.
    return cv.addWeighted(image, 1.0, line_image, 0.95, 0.0)
