import cv2 as cv
import numpy as np
import roi
import drawing as draw
import extrapolation as ex
# from skvideo.io import FFmpegWriter

# output = 'video/out1.mp4'
filename = 'video/highway1.mp4'
cap = cv.VideoCapture(filename)

# writer = FFmpegWriter(output, outputdict={'-r': 24})
# writer = FFmpegWriter(output)

while True:
    _, frame = cap.read()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    _, thr = cv.threshold(gray, 100, 255, cv.THRESH_BINARY)
    gray = cv.GaussianBlur(gray, (5, 5), 1)
    #edges = cv.Canny(gray, 200, 255)

    points = np.array([[[72, 268], [269, 175], [352, 175],
                        [462, 262]]], dtype=np.int32)
    mask = roi.mask(points, frame=thr)
    masked_image = roi.applyMask(thr, mask)
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (2, 2))
    masked_image = cv.morphologyEx(masked_image, cv.MORPH_OPEN, kernel)
    masked_image = cv.Sobel(masked_image, cv.CV_8UC1, 1, 0, ksize=3)
    cv.imshow('threshold', masked_image)
    # lines = cv.HoughLines(masked_image, 2, np.pi/180, 40,
    #                      max_theta=np.pi/2, min_theta=-np.pi/2)
    lines = cv.HoughLinesP(masked_image, rho=1, theta=np.pi/180, threshold=20,
                    minLineLength=20, maxLineGap=100)
    left_lines, right_lines = ex.separateLines(lines)

    leftLine = ex.lstsqLine(left_lines)
    rightLine = ex.lstsqLine(right_lines)
    frame = draw.fillLane(leftLine, rightLine, frame)
    cv.imshow('highway in Moscow', frame)
    print('*'*20)
#    try:
#        writer.writeFrame(cv.cvtColor(frame, cv.COLOR_BGR2RGB))
#    except:
#        writer.close()
#        break
    k = cv.waitKey(30) & 0xff
    if k == 27:
        break

# writer.close()
cap.release()
cv.destroyAllWindows()
