"""
README
======
This file contains Python codes.
======
"""

# Enter your account ID and API key here.
account_id = 6858884
key = "4c7718c7e03d472c2369abf1cb7ceddb-" \
      "142b7d845d68844e853bb95c63f1c8b9"

""" Fetch rates """
import oandapy

oanda = oandapy.API(environment="practice", access_token=key)
response = oanda.get_prices(instruments="EUR_USD")
print response

prices = response["prices"]
bidding_price = float(prices[0]["bid"])
asking_price = float(prices[0]["ask"])
instrument = prices[0]["instrument"]
time = prices[0]["time"]
print "[%s] %s bid=%s ask=%s" % (
    time, instrument, bidding_price, asking_price)

""" Send an order """
from datetime import datetime, timedelta

# set the trade to expire after one day
trade_expire = datetime.now() + timedelta(days=1)
trade_expire = trade_expire.isoformat("T") + "Z"

response = oanda.create_order(
    account_id,
    instrument="EUR_USD",
    units=1000,
    side="sell",  # "buy" or "sell"
    type="limit",
    price=1.105,
    expiry=trade_expire)
print response