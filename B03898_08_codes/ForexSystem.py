"""
README
======
This file contains Python codes.
======
"""

"""
Implementing the trend-following algorithm
for trading foreign currencies
"""
import oandapy
from datetime import datetime
import pandas as pd


class ForexSystem(oandapy.Streamer):
    def __init__(self, *args, **kwargs):
        oandapy.Streamer.__init__(self, *args, **kwargs)
        self.oanda = oandapy.API(kwargs["environment"],
                                 kwargs["access_token"])

        self.instrument = None
        self.account_id = None
        self.qty = 0
        self.resample_interval = '10s'
        self.mean_period_short = 5
        self.mean_period_long = 20
        self.buy_threshold = 1.0
        self.sell_threshold = 1.0

        self.prices = pd.DataFrame()
        self.beta = 0
        self.is_position_opened = False
        self.opening_price = 0
        self.executed_price = 0
        self.unrealized_pnl = 0
        self.realized_pnl = 0
        self.position = 0
        self.dt_format = "%Y-%m-%dT%H:%M:%S.%fZ"

    def begin(self, **params):
        self.instrument = params["instruments"]
        self.account_id = params["accountId"]
        self.qty = params["qty"]
        self.resample_interval = params["resample_interval"]
        self.mean_period_short = params["mean_period_short"]
        self.mean_period_long = params["mean_period_long"]
        self.buy_threshold = params["buy_threshold"]
        self.sell_threshold = params["sell_threshold"]

        self.start(**params)  # Start streaming prices

    def on_success(self, data):
        time, symbol, bid, ask = self.parse_tick_data(
            data["tick"])
        self.tick_event(time, symbol, bid, ask)

    def parse_tick_data(self, dict_data):
        time = datetime.strptime(dict_data["time"],
                                 self.dt_format)
        ask = float(dict_data["ask"])
        bid = float(dict_data["bid"])
        instrument = dict_data["instrument"]
        return time, instrument, bid, ask

    def tick_event(self, time, symbol, bid, ask):
        midprice = (ask+bid)/2.
        self.prices.loc[time, symbol] = midprice

        resampled_prices = self.prices.resample(
            self.resample_interval,
            how='last',
            fill_method="ffill")

        mean_short = resampled_prices.tail(
            self.mean_period_short).mean()[0]
        mean_long = resampled_prices.tail(
            self.mean_period_long).mean()[0]
        self.beta = mean_short / mean_long

        self.perform_trade_logic(self.beta)
        self.calculate_unrealized_pnl(bid, ask)
        self.print_status()

    def perform_trade_logic(self, beta):

        if beta > self.buy_threshold:
            if not self.is_position_opened \
                    or self.position < 0:
                self.check_and_send_order(True)

        elif beta < self.sell_threshold:
            if not self.is_position_opened \
                    or self.position > 0:
                self.check_and_send_order(False)

    def check_and_send_order(self, is_buy):
        if self.place_market_order(self.qty, is_buy):
            # Update position upon successful order
            if is_buy:
                self.position += self.qty
            else:
                self.position -= self.qty

            if self.position == 0:
                self.is_position_opened = False
                self.calculate_realized_pnl(is_buy)
            else:
                self.opening_price = self.executed_price
                self.is_position_opened = True

    def calculate_realized_pnl(self, is_buy):
        self.realized_pnl += self.qty * (
            (self.opening_price - self.executed_price)
            if is_buy else
            (self.executed_price - self.opening_price))

    def calculate_unrealized_pnl(self, bid, ask):
        if self.is_position_opened:
            # Retrieve position from server
            pos = self.oanda.get_position(self.account_id,
                                          self.instrument)
            units = pos["units"]
            side = pos["side"]
            avg_price = float(pos["avgPrice"])

            self.unrealized_pnl = units * (
                (bid - avg_price)
                if (side == "buy")
                else (avg_price - ask))
        else:
            self.unrealized_pnl = 0

    def place_market_order(self, qty, is_buy):
        side = "buy" if is_buy else "sell"
        response = self.oanda.create_order(
            account_id,
            instrument=self.instrument,
            units=qty,
            side=side,
            type='market')

        if response is not None:
            self.executed_price = float(response["price"])
            print "Placed order %s %s %s at market." % (side, qty, self.instrument)
            return True  # Order is successful

        return False  # Order is unsuccessful

    def print_status(self):
        print "[%s] %s pos=%s beta=%s RPnL=%s UPnL=%s" % (
            datetime.now().time(),
            self.instrument,
            self.position,
            round(self.beta, 5),
            self.realized_pnl,
            self.unrealized_pnl)

    def on_error(self, data):
        print data
        self.disconnect()

if __name__ == "__main__":
    key = "4c7718c7e03d472c2369abf1cb7ceddb-" \
          "142b7d845d68844e853bb95c63f1c8b9"
    account_id = 6858884
    system = ForexSystem(environment="practice", access_token=key)
    system.begin(accountId=account_id,
                 instruments="EUR_USD",
                 qty=1000,
                 resample_interval="10s",
                 mean_period_short=5,
                 mean_period_long=20,
                 buy_threshold=1.,
                 sell_threshold=1.)