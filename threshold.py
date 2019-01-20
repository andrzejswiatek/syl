import matplotlib.pyplot as plt
from skimage import data, filters, io
from skimage.color import rgb2grey
fig, ax = plt.subplots(nrows=2, ncols=2)

#image = data.coins()
image = rgb2grey(io.imread('images/tasma3.jpg'))
edges = filters.sobel(image)

#low = 0.1
#high = 0.35
low = 0.1
high = 0.9

lowt = (edges > low).astype(int)
hight = (edges > high).astype(int)
hyst = filters.apply_hysteresis_threshold(edges, low, high)

ax[0, 0].imshow(image, cmap='gray')
ax[0, 0].set_title('Original image')

ax[0, 1].imshow(edges, cmap='magma')
ax[0, 1].set_title('Sobel edges')

ax[1, 0].imshow(lowt, cmap='magma')
ax[1, 0].set_title('Low threshold')

ax[1, 1].imshow(hight + hyst, cmap='magma')
ax[1, 1].set_title('Hysteresis threshold')

for a in ax.ravel():
    a.axis('off')

plt.tight_layout()
plt.show()