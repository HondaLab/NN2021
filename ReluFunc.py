import numpy as np
import matplotlib.pylab as plt

def relu_function(x):
  return np.where(x<=0,0,x)

x = np.linspace(-5, 5)
y = relu_fanction(x)

plt.plot(x, y)
plt.show()
