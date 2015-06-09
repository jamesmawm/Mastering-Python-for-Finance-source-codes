"""
README
======
This file contains Python codes.
======
"""

def zero_coupon_bond(par, y, t):
    """
    Price a zero coupon bond.
    
    Par - face value of the bond.
    y - annual yield or rate of the bond.
    t - time to maturity in years.
    """
    return par/(1+y)**t

print zero_coupon_bond(100, 0.05, 5)