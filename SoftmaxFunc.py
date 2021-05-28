import numpy as np

def softmax_function(x):
  return np.exp(x)/np.sum(np.exp(x))

y = softmax_function(np.array([1,2,3]))
print(y)

