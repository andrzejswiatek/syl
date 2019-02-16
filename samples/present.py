import matplotlib.pyplot as plt
from skimage import io

image = io.imread('images/tasma.jpg')
plt.imshow(image)
plt.tight_layout()
plt.show()