import numpy as np
import cv2

def nothing(x):
    pass

def create_trackbars():
    cv2.createTrackbar('min', 'frame', 0, 255, nothing)
    cv2.createTrackbar('max', 'frame', 0, 255, nothing)
    cv2.setTrackbarPos('min', 'frame', 30)
    cv2.setTrackbarPos('max', 'frame', 255)

def draw_lines(img, min_val=0, max_val=255):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, min_val, max_val, apertureSize=5)
    min_line_length = 100
    max_line_gap = 10
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, min_line_length, max_line_gap)
    for x1, y1, x2, y2 in lines[0]:
        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

def draw_contours(img):
    imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(imgray,50,200,0)
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img, contours, -1, (255,0,0), 3)

cap = cv2.VideoCapture(r'D:\Projekty\MachineLearning\Sylwek\tasma.mp4')
# bound = ([60, 60, 40], [250, 250, 230])
bound = ([40, 40, 70], [100, 210, 210])

cv2.namedWindow('frame')
create_trackbars()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower = np.array(bound[0], dtype="uint8")
    upper = np.array(bound[1], dtype="uint8")
    mask = cv2.inRange(hsv, lower, upper)
    new_image = cv2.bitwise_and(frame, frame, mask=mask)
    min_val = cv2.getTrackbarPos('min', 'frame')
    max_val = cv2.getTrackbarPos('max', 'frame')
    #draw_lines(new_image, min_val, max_val)
    draw_contours(new_image)
    cv2.imshow('frame', new_image)
    # cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
