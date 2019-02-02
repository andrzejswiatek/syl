import cv2
import copy
import numpy as np
import matplotlib.pyplot as plt
from skimage import img_as_float

image = cv2.imread('images/tasma.jpg')

#bound = ([40,40,70], [100,210,210])
bound = ([60, 60, 40], [250, 250, 230])

#istotna jest relacja pomiedzy kolorami - żółtawa carakterystyka
def in_interval(p, a, b):
    threshold = 20
    if a[0] < p[0] < b[0] and a[1] < p[1] < b[1] and a[2] < p[2] < b[2]\
            and p[0] > p[2] + threshold and p[1] > p[2] + threshold:
        return True
    return  False

def threshold_slow(T, img):
    # grab the image dimensions
    h = img.shape[0]
    w = img.shape[1]
    print ('Size:', h, w)
    # loop over the image, pixel by pixel
    for y in range(0, h):
        for x in range(0, w):
            # threshold the pixel
            if in_interval(img[y, x], bound[0], bound[1]):
                img[y, x] = [255, 0, 0]
            else:
                img[y, x] = [0, 0, 0]
            #img[y, x] = 255 if img[y, x] >= T else 0
    return img

def adjust_mask(mask, img):
    h = img.shape[0]
    w = img.shape[1]
    for y in range(0, h):
        for x in range(0, w):
            # threshold the pixel
            if mask[y, x] == 255 and not in_interval(img[y, x], bound[0], bound[1]):
                mask[y, x] = 0
    return mask

#hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
#lower = np.array(bound[0], dtype="uint8")
#upper = np.array(bound[1], dtype="uint8")
#mask = cv2.inRange(hsv, lower, upper)
#mask = adjust_mask(mask, image)
new_image = threshold_slow(3, copy.copy(image))
#new_image = cv2.bitwise_and(hsv, hsv, mask)
fig, ax = plt.subplots(ncols=2, nrows=1, sharex=True, sharey=True)
ax[0].imshow(image)
ax[1].imshow(new_image)
plt.tight_layout()
plt.show()
