import matplotlib.pyplot as plt
from skimage.filters.rank import otsu
from skimage.filters import threshold_otsu
from skimage.filters import rank
import numpy as np
from skimage.morphology import disk
from skimage import io, img_as_ubyte

#n = 100
#theta = np.linspace(0, 10 * np.pi, n)
#x = np.sin(theta)
#m = (np.tile(x, (n, 1)) * np.linspace(0.1, 1, n) * 128 + 128).astype(np.uint8)
radius = 10
m = img_as_ubyte(io.imread('images/tasma3.jpg', as_gray=True))
t = rank.otsu(m, disk(radius))

fig, ax = plt.subplots(ncols=2, figsize=(10, 5),
                       sharex=True, sharey=True)

ax[0].imshow(m, cmap=plt.cm.gray)
ax[0].set_title('Original')

ax[1].imshow(m >= t, interpolation='nearest', cmap=plt.cm.gray)
ax[1].set_title('Local Otsu ($r=%d$)' % radius)

for a in ax:
    a.axis('off')

plt.tight_layout()
plt.show()