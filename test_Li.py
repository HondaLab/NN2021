import numpy as np
import matplotlib.pyplot as plt

def step_function(x):
    return x 
    
x=np.linspace(-5,5)
y=step_function(x)

plt.plot(x,y)
plt.show()
