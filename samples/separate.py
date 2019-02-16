# import the necessary packages
import numpy as np
import cv2
import matplotlib.pyplot as plt
from skimage import img_as_float
from skimage.feature import canny
from skimage.color import rgb2grey
from skimage.transform import (probabilistic_hough_line)
from skimage import measure

def draw_lines(img, ax, sigma=1):
    edges = canny(img, sigma)
    lines = probabilistic_hough_line(edges, line_length=100, line_gap=50)
    ax.imshow(edges * 0)
    ax.imshow(edges)
    for line in lines:
        print(line)
        p0, p1 = line
        ax.plot((p0[0], p1[0]), (p0[1], p1[1]))

def draw_contours(img, ax):
    contours = measure.find_contours(img, 0.34)
    for n, contour in enumerate(contours):
        ax.plot(contour[:, 1], contour[:, 0], linewidth=2)


# load the image
image = cv2.imread('images/tasma.jpg')
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

rgb_start1 = [50, 50, 100]
rgb_end1 = [100, 250, 250]
rgb_start2 = [50, 100, 90]
rgb_end2 = [90, 130, 130]

rgb_start3 = [40,40,70]
rgb_end3 = [200,200,255]

# define the list of boundaries
boundaries = [
    #(rgb_start1, rgb_end1),
    #(rgb_start2, rgb_end2),
    #(rgb_start3, rgb_end3)

    #([40,40,70], [140,190,190]),
    #([40,40,70], [120,200,200]),

    # najlepsze ustawienie
    ([40,40,70], [100,210,210])
    #([78,113, 115], [81, 121, 120])
    #([0,0,0], [150,150,150])
]


fig, ax = plt.subplots(ncols=2, nrows=2, sharex=True, sharey=True)
image_in = img_as_float(image)
ax[0][0].imshow(image_in)
# loop over the boundaries
for (lower, upper) in boundaries:
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")

    #mask = cv2.inRange(image, lower, upper)
    mask = cv2.inRange(hsv, lower, upper)
    output = cv2.bitwise_and(image, image, mask=mask)
    # show the images
    #cv2.imshow('image', image)
    #cv2.imshow('output', output)
    #cv2.imshow('mask', mask)
    #cv2.waitKey(0)
    image_out = img_as_float(output)
    mask_out = img_as_float(mask)
    ax[0][1].imshow(image_out)
    #ax[0][2].imshow(mask_out)
    ax[1][0].imshow(image_out)
    draw_lines(rgb2grey(mask_out), ax[1][0])
    ax[1][1].imshow(image_out)
    draw_contours(rgb2grey(mask_out), ax[1][1])
    plt.tight_layout()
    plt.show()