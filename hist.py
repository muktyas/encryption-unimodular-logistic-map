import numpy as np
from PIL import Image
from matplotlib import pyplot as plt

im = Image.open('morning.png')  
mgb = np.array(im)

r,g,b = mgb[:,:,0], mgb[:,:,1], mgb[:,:,2]
#rku = Image.fromarray(r)
#gku = Image.fromarray(g)
bku = Image.fromarray(b)
#rhis = rku.histogram()
#ghis = gku.histogram()
bhis = bku.histogram()
plt.style.use('ggplot')
plt.bar(range(256), bhis, edgecolor = "none")
plt.savefig('histogram b.png')
plt.show()
