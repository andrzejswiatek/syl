import numpy as np

from skimage.transform import (hough_line, hough_line_peaks,
                               probabilistic_hough_line)
from skimage.feature import canny
from skimage import data, io

import matplotlib.pyplot as plt
from matplotlib import cm

image = io.imread('images/tasma3.png', as_gray=True)
# Constructing test image
#image = np.zeros((100, 100))
#idx = np.arange(25, 75)
#image[idx[::-1], idx] = 255
#image[idx, idx] = image = io.imread('images/tasma.png', as_gray=True);
# Classic straight-line Hough transform


def draw_canny(sigma):
    h, theta, d = hough_line(image)

    # Line finding using the Probabilistic Hough Transform
    #image = data.camera()
    #edges = canny(image, 2, 1, 25)
    edges = canny(image, sigma)
    lines = probabilistic_hough_line(edges, line_length=100,
                                     line_gap=50)

    # Generating figure 2
    fig, axes = plt.subplots(3, 1, figsize=(15, 5), sharex=True, sharey=True)
    ax = axes.ravel()

    ax[0].imshow(image, cmap=cm.gray)
    ax[0].set_title('Input image')

    ax[1].imshow(edges, cmap=cm.gray)
    ax[1].set_title('Canny edges ' + str(sigma))

    ax[2].imshow(edges * 0)
    for line in lines:
        p0, p1 = line
        ax[2].plot((p0[0], p1[0]), (p0[1], p1[1]))
    ax[2].set_xlim((0, image.shape[1]))
    ax[2].set_ylim((image.shape[0], 0))
    ax[2].set_title('Probabilistic Hough')

    for a in ax:
        a.set_axis_off()

    plt.tight_layout()
    plt.show()

draw_canny(1)