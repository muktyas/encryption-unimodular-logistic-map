from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
import os

#gb = raw_input("insert image with extension here: ")
gb = 'Airplane.png'
namasaja = os.path.splitext(gb)[0]
im=Image.open(gb)

a = np.array(im.getdata())

print im.getdata
#b = a[:,:,0]
#print b
plt.style.use('seaborn')
plt.hist(a, bins=range(256), edgecolor='none')
plt.title("histogram of "+ namasaja+" layer R")
plt.xlim(0,255)	
plt.savefig('histogram of ' + namasaja + '.png')
plt.show()
