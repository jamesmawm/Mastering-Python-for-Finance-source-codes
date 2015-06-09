"""
README
======
This file contains Python codes.
======
"""

""" Simulate interest rate path by the Rendleman-Barter model """
import numpy as np

def rendleman_bartter(r0, theta, sigma, T=1.,N=10,seed=777):        
    np.random.seed(seed)
    dt = T/float(N)    
    rates = [r0]
    for i in range(N):
        dr = theta*rates[-1]*dt + \
             sigma*rates[-1]*np.random.normal()
        rates.append(rates[-1] + dr)
    return range(N+1), rates

if __name__ == "__main__":
    x, y = rendleman_bartter(0.01875, 0.01, 0.012, 10., 200)

    import matplotlib.pyplot as plt
    plt.plot(x,y)
    plt.show()