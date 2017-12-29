import cv2 as cv
import numpy as np
import roi
import drawing as draw
import extrapolation as ex

filename = 'video/highway1.mp4'
cap = cv.VideoCapture(filename)

framecnt = 0
llinecnt = 0
rlinecnt = 0

while True:
    _, frame = cap.read()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    _, thr = cv.threshold(gray, 100, 255, cv.THRESH_BINARY)
    edges = cv.Canny(thr, 0, 166)

    points = np.array([[[72, 268], [269, 190], [352, 190],
                        [462, 262]]], dtype=np.int32)
    mask = roi.mask(points, frame=edges)
    masked_image = roi.applyMask(edges, mask)
    # lines = cv.HoughLines(masked_image, 2, np.pi/180, 40,
    #                      max_theta=np.pi/2, min_theta=-np.pi/2)
    lines = cv.HoughLinesP(masked_image, rho=2, theta=np.pi/180, threshold=20,
                    minLineLength=20, maxLineGap=100)
    left_lines, right_lines = ex.separateLines(lines)
    left_mean = ex.averageLines(left_lines)
    right_mean = ex.averageLines(right_lines)
    framecnt += 1
    llinecnt += len(left_mean)
    rlinecnt += len(right_mean)
    leftLine = ex.lstsqLine(left_lines)
    rightLine = ex.lstsqLine(right_lines)
    frame = draw.drawlinesP(frame, leftLine, (0, 51, 255), 3)
    frame = draw.drawlinesP(frame, rightLine, (102, 153, 51), 3)
    cv.imshow('highway in Moscow', frame)
    k = cv.waitKey(30) & 0xff
    if k == 27:
        break

print(rlinecnt, llinecnt, framecnt)
cap.release()
cv.destroyAllWindows()
