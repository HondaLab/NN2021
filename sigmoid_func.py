import numpy as np
#import matplotlib.pyplot as plt
import matplotlib.pylab as plt

def sigmoid_function(x):
    return 2/(1+np.exp(-x))
    
x=np.linspace(-3,3)
y=sigmoid_function(x)

plt.plot(x,y)
plt.show()
