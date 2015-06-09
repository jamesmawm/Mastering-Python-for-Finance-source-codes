"""
README
======
This file contains Python codes.
======
"""

import datetime as dt
import numpy as np
import pandas.io.data as web
from scipy.stats import norm


def calculate_daily_VaR(P, prob, mean, sigma, 
                        days_per_year=252.):
    min_ret = norm.ppf(1-prob, 
                       mean/days_per_year, 
                       sigma/np.sqrt(days_per_year))
    return P - P*(min_ret+1)

if __name__ == "__main__":
    start = dt.datetime(2013, 12, 1)
    end = dt.datetime(2014, 12, 1)
    
    prices = web.DataReader("AAPL", "yahoo", start, end)
    returns = prices["Adj Close"].pct_change().dropna()

    portvolio_value = 100000000.00
    confidence = 0.95
    mu = np.mean(returns)
    sigma = np.std(returns)
    
    VaR = calculate_daily_VaR(portvolio_value, confidence,
                              mu, sigma)
    print "Value-at-Risk:", round(VaR, 2)