import cv2 as cv
import numpy as np
import roi
import drawing as draw
import extrapolation as ex
filename = 'video/highway1.mp4'
cap = cv.VideoCapture(filename)

while True:
    _, frame = cap.read()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    _, thr = cv.threshold(gray, 100, 255, cv.THRESH_BINARY)
    edges = cv.Canny(thr, 0, 166)

    points = np.array([[[72, 268], [269, 179], [352, 187],
                        [462, 262]]], dtype=np.int32)
    mask = roi.mask(points, frame=edges)
    masked_image = roi.applyMask(edges, mask)
    # lines = cv.HoughLines(masked_image, 2, np.pi/180, 40,
    #                      max_theta=np.pi/2, min_theta=-np.pi/2)
    lines = cv.HoughLinesP(masked_image, rho=2, theta=np.pi/180, threshold=20,
                    minLineLength=20, maxLineGap=100)
    
    # draw.drawlinesP(frame, lines, (0, 240, 0), 2)
    ex.draw_lane_lines(frame, ex.lane_lines(frame, lines))
    cv.imshow('highway in Moscow', frame)
    # cv.imshow('edges', thr)
    k = cv.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv.destroyAllWindows()
