"""
README
======
This file contains Python codes.
======
"""

import numpy as np

""" Get zero coupon bond price by Vasicek model """
def exact_zcb(theta, kappa, sigma, tau, r0=0.):
    B = (1 - np.exp(-kappa*tau)) / kappa
    A = np.exp((theta-(sigma**2)/(2*(kappa**2))) *
               (B-tau) - (sigma**2)/(4*kappa)*(B**2))
    return A * np.exp(-r0*B)

import math
def exercise_value(K, R, t):
    return K*math.exp(-R*t)


if __name__ == "__main__":
    Ts = np.r_[0.0:25.5:0.5]
    zcbs = [exact_zcb(0.5, 0.02, 0.03, t, 0.015) for t in Ts]

    import matplotlib.pyplot as plt
    plt.title("Zero Coupon Bond (ZCB) Values by Time")
    plt.plot(Ts, zcbs, label='ZCB')
    plt.ylabel("Value ($)")
    plt.xlabel("Time in years")
    plt.legend()
    plt.grid(True)
    plt.show()

    Ks = [exercise_value(0.95, 0.015, t) for t in Ts]
    plt.title("Zero Coupon Bond (ZCB) "
              "and Strike (K) Values by Time")
    plt.plot(Ts, zcbs, label='ZCB')
    plt.plot(Ts, Ks, label='K', linestyle="--", marker=".")
    plt.ylabel("Value ($)")
    plt.xlabel("Time in years")
    plt.legend()
    plt.grid(True)
    plt.show()

