"""
README
======
This file contains Python codes.
======
"""


import numpy as np
import scipy.stats as stats
import pythoncom

class BlackScholes:
    _public_methods_ = ["call_pricer", "put_pricer"]
    _reg_progid_ = "BlackScholes.Pricer"
    _reg_clsid_ =  pythoncom.CreateGuid()

    def d1(self, S0, K, r, T, sigma, div):
        return (np.log(S0/K) + ((r-div) + sigma**2 / 2) * T)/ \
               (sigma * np.sqrt(T))

    def d2(self, S0, K, r, T, sigma, div):
        return (np.log(S0 / K) + ((r-div) - sigma**2 / 2) * T) / \
               (sigma * np.sqrt(T))

    def call_pricer(self, S0, K, r, T, sigma, div):
        d1 = self.d1(S0, K, r, T, sigma, div)
        d2 = self.d2(S0, K, r, T, sigma, div)
        return S0 * np.exp(-div * T) * stats.norm.cdf(d1) \
               - K * np.exp(-r * T) * stats.norm.cdf(d2)

    def put_pricer(self, S0, K, r, T, sigma, div):
        d1 = self.d1(S0, K, r, T, sigma, div)
        d2 = self.d2(S0, K, r, T, sigma, div)
        return K * np.exp(-r * T) * stats.norm.cdf(-d2) \
               - S0 * np.exp(-div * T) *stats.norm.cdf(-d1)

if __name__ == "__main__":
    # Run "python binomial_tree_am.py"
    #   to register the COM server.
    # Run "python binomial_tree_am.py --unregister"
    #   to unregister it.
    print "Registering COM server..."
    import win32com.server.register
    win32com.server.register.UseCommandLine(BlackScholes)