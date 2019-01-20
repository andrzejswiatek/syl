import cv2
import numpy as np
from skimage import img_as_float
import matplotlib.pyplot as plt

img = cv2.imread('images/tasma.png')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,50,150,apertureSize = 3)
minLineLength = 100
maxLineGap = 10
lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength,maxLineGap)
for x1,y1,x2,y2 in lines[0]:
    cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)

fig, ax = plt.subplots(ncols=1, nrows=1, sharex=True, sharey=True,
                       figsize=(8, 4))

im2 = img_as_float(img)
ax.imshow(im2, cmap=plt.cm.gray)
plt.tight_layout()
plt.show()