import numpy as np
import matplotlib.pylab as plt

def leaky_relu_function(x):
  return np.where(x<=0,0.01*x,x)

x = np.linspace(-5, 5)
y = leaky_relu_fanction(x)

plt.plot(x, y)
plt.show()
