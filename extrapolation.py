import numpy as np
import cv2 as cv


def separateLines(lines):
    left_lines = []
    left_dist = []
    right_lines = []
    right_dist = []
    left_lane = None
    right_lane = None
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                if x2 == x1:
                    continue
                else:
                    slope = (y2-y1)/(x2-x1)
                    intercept = y1 - slope*x1
                    length = np.sqrt((x2-x1)**2 + (y2-y1)**2)
                    if slope < 0:
                        left_lines.append((slope, intercept))
                        left_dist.append(length)
                    else:
                        right_lines.append((slope, intercept))
                        right_dist.append(length)
    
        # computing mean
        left_lane = np.dot(left_dist, left_lines) / np.sum(
                left_dist) if len(left_dist) > 0 else None
        right_lane = np.dot(right_dist, right_lines) / np.sum(
                right_dist) if len(right_dist) > 0 else None
    return left_lane, right_lane


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
    
    y1 = image.shape[0] # bottom of the image
    y2 = y1*0.6         # slightly lower than the middle

    left_line  = make_line_points(y1, y2, left_lane)
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