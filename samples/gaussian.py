import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage as ndi

from skimage import feature, io

# Generate noisy image of a square
#im = np.zeros((128, 128))
#im[32:-32, 32:-32] = 1
#im = ndi.rotate(im, 15, mode='constant')
#im = ndi.gaussian_filter(im, 4)
#im += 0.2 * np.random.random(im.shape)

im = io.imread('images/tasma.jpg', as_gray=True)
# Compute the Canny filter for two values of sigma
edges1 = feature.canny(im)

edges = [edges1]
# display results
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(8, 3),
                                    sharex=True, sharey=True)

axes[0].imshow(im, cmap=plt.cm.gray)
axes[0].axis('off')
axes[0].set_title('noisy image', fontsize=20)

for e in range(1, len(edges)):
    axes[e].imshow(edges[e], cmap=plt.cm.gray)
    axes[e].axis('off')
    axes[e].set_title('Canny filter, $\sigma=1$', fontsize=20)


fig.tight_layout()

plt.show()