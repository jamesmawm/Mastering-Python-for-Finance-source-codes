"""
README
======
This file contains Python codes.
======
"""

""" Price an option by the binomial CRR model """
from BinomialTreeOption import BinomialTreeOption
import math


class BinomialCRROption(BinomialTreeOption):

    def _setup_parameters_(self):
        self.u = math.exp(self.sigma * math.sqrt(self.dt))
        self.d = 1./self.u
        self.qu = (math.exp((self.r-self.div)*self.dt) -
                   self.d)/(self.u-self.d)
        self.qd = 1-self.qu

if __name__ == "__main__":
    from BinomialCRROption import BinomialCRROption
    eu_option = BinomialCRROption(
        50, 50, 0.05, 0.5, 2,
        {"sigma": 0.3, "is_call": False})
    print "European put: %s" % eu_option.price()

    am_option = BinomialCRROption(
        50, 50, 0.05, 0.5, 2,
        {"sigma": 0.3, "is_call": False, "is_eu": False})
    print "American put: %s" % am_option.price()
