import numpy as np
import matplotlib.pylab as plt

def tanh_function(x):
  return np.tanh(x)

x = np.linspace(-5, 5)
y = tanh_fanction(x)

plt.plot(x, y)
plt.show()
