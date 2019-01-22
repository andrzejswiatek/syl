import matplotlib.pyplot as plt
import numpy as np
from skimage import data, io, color
from skimage.color import rgb2lab, rgb2hsv
from matplotlib.colors import LinearSegmentedColormap

# Create an artificial color close to the original one
rgb_start = (213, 213, 213)
rgb_end = (45, 70, 255)

cmap_hema = LinearSegmentedColormap.from_list('mycmap', ['lightblue', 'darkblue'])
#cmap_hema = LinearSegmentedColormap.from_list('mycmap', [rgb_start, rgb_end])
cmap_dab = LinearSegmentedColormap.from_list('mycmap', ['white', 'saddlebrown'])
cmap_eosin = LinearSegmentedColormap.from_list('mycmap', ['darkviolet', 'white'])

ihc_rgb = io.imread('images/tasma.jpg')
ihc_hed = rgb2lab(ihc_rgb)

fig, axes = plt.subplots(2, 2, figsize=(7, 6), sharex=True, sharey=True)
ax = axes.ravel()

ax[0].imshow(ihc_rgb)
ax[0].set_title("Original image")

ax[1].imshow(ihc_hed[:, :, 0], cmap=cmap_hema)
ax[1].set_title("Hematoxylin")

ax[2].imshow(ihc_hed[:, :, 1], cmap=cmap_eosin)
ax[2].set_title("Eosin")

ax[3].imshow(ihc_hed[:, :, 2], cmap=cmap_dab)
ax[3].set_title("DAB")

for a in ax.ravel():
    a.axis('off')

fig.tight_layout()
plt.show()