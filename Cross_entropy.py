import numpy as np

def cross_entropy(y,t):
    return -np.sum(t*np.log(y+1e-7))
