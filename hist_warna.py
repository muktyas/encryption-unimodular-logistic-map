import numpy as np
from PIL import Image
from matplotlib import pyplot as plt

im = Image.open('ciphertext_morning.png')  
mgb = np.array(im)

r,g,b = mgb[:,:,0], mgb[:,:,1], mgb[:,:,2]
rku = Image.fromarray(r)
gku = Image.fromarray(g)
bku = Image.fromarray(b)
rhis = rku.histogram()
ghis = gku.histogram()
bhis = bku.histogram()
plt.style.use('ggplot')
plt.subplot(3,1,1)
plt.bar(range(256), rhis, edgecolor = "none")
plt.title("histogram R")
plt.xlim(0,255)
plt.subplot(3,1,2)
plt.bar(range(256), ghis, edgecolor = "none")
plt.title("histogram G")
plt.xlim(0,255)
plt.subplot(3,1,3)
plt.bar(range(256), bhis, edgecolor = "none")
plt.title("histogram B")
plt.xlim(0,255)
plt.tight_layout()
plt.savefig('histogram rgb.png')
plt.show()
