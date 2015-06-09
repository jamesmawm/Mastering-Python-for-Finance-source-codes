"""
README
======
This file contains Python codes.
======
"""

""" Price an option by the Leisen-Reimer tree """
from BinomialTreeOption import BinomialTreeOption
import math


class BinomialLROption(BinomialTreeOption):

    def _setup_parameters_(self):
        odd_N = self.N if (self.N%2 == 1) else (self.N+1)
        d1 = (math.log(self.S0/self.K) +
              ((self.r-self.div) +
               (self.sigma**2)/2.) *
              self.T) / (self.sigma * math.sqrt(self.T))
        d2 = (math.log(self.S0/self.K) +
              ((self.r-self.div) -
               (self.sigma**2)/2.) *
              self.T) / (self.sigma * math.sqrt(self.T))
        pp_2_inversion = \
            lambda z, n: \
            .5 + math.copysign(1, z) * \
            math.sqrt(.25 - .25 * math.exp(
                -((z/(n+1./3.+.1/(n+1)))**2.)*(n+1./6.)))
        pbar = pp_2_inversion(d1, odd_N)

        self.p = pp_2_inversion(d2, odd_N)
        self.u = 1/self.df * pbar/self.p
        self.d = (1/self.df - self.p*self.u)/(1-self.p)
        self.qu = self.p
        self.qd = 1-self.p

if __name__ == "__main__":
    from BinomialLROption import BinomialLROption
    eu_option = BinomialLROption(
        50, 50, 0.05, 0.5, 3,
        {"sigma": 0.3, "is_call": False})
    print "European put: %s" % eu_option.price()

    am_option = BinomialLROption(
        50, 50, 0.05, 0.5, 3,
        {"sigma": 0.3, "is_call": False, "is_eu": False})
    print "American put: %s" % am_option.price()