#matplotlib inline

import numpy as np
import matplotlib.pyplot as plt

X = np.arange(-1.0,1.0,0.2)
Y = np.arange(-1.0,1.0,0.2)

Z = np.zeros((10,10))

w_im = np.array([[4.0,4.0],
                    [4.0,4.0]])

w_mo = np.array([[1.0],
                    [-1.0]])

b_im = np.array(([3.0,-3.0]))
b_mo = np.array([0.1])

def middle_layer(x,w,b):
    u = np.dot(x,w) + b
    return 1/(1+np.exp(-u))

def output_layer(x,w,b):
    u = np.dot(x,w) + b
    return u

for i in range(10):
   for j in range(10):

    inp = np.array([X[i],Y[j]])
    mid = middle_layer(inp,w_im,b_im)
    out = output_layer(mid,w_mo,b_mo)

    Z[i][j] = out[0]

plt.imshow(Z, "gray",vmin = 0.0, vmax =1.0)
plt.colorbar()
plt.show()
