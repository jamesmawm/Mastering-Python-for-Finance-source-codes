"""
README
======
This file contains Python codes.
======
"""

""" Get bond price from YTM """
def bond_price(par, T, ytm, coup, freq=2):
    freq = float(freq)
    periods = T*freq
    coupon = coup/100.*par/freq
    dt = [(i+1)/freq for i in range(int(periods))]
    price = sum([coupon/(1+ytm/freq)**(freq*t) for t in dt]) + \
            par/(1+ytm/freq)**(freq*T)
    return price


if __name__ == "__main__":
    from bond_ytm import bond_ytm
    ytm = bond_ytm(95.0428, 100, 1.5, 5.75, 2)
    print bond_price(100, 1.5, ytm, 5.75, 2)
