"""
README
======
This file contains Python codes.
======
"""

""" Implementing the Mean-Reverting Algorithm """
from ib.ext.Contract import Contract
from ib.ext.Order import Order
from ib.opt import Connection, message
import time
import pandas as pd
import datetime as dt


class AlgoSystem:
    def __init__(self, symbol, qty, resample_interval,
                 averaging_period=5, port=7496):
        self.client_id = 1
        self.order_id = 1
        self.qty = qty
        self.symbol_id, self.symbol = 0, symbol
        self.resample_interval = resample_interval
        self.averaging_period = averaging_period
        self.port = port
        self.tws_conn = None
        self.bid_price, self.ask_price = 0, 0
        self.last_prices = pd.DataFrame(columns=[self.symbol_id])
        self.average_price = 0
        self.is_position_opened = False
        self.account_code = None
        self.unrealized_pnl, self.realized_pnl = 0, 0
        self.position = 0

    def error_handler(self, msg):
        if msg.typeName == "error" and msg.id != -1:
            print "Server Error:", msg

    def server_handler(self, msg):
        if msg.typeName == "nextValidId":
            self.order_id = msg.orderId
        elif msg.typeName == "managedAccounts":
            self.account_code = msg.accountsList
        elif msg.typeName == "updatePortfolio" \
                and msg.contract.m_symbol == self.symbol:
            self.unrealized_pnl = msg.unrealizedPNL
            self.realized_pnl = msg.realizedPNL
            self.position = msg.position
        elif msg.typeName == "error" and msg.id != -1:
            return

    def tick_event(self, msg):
        if msg.field == 1:
            self.bid_price = msg.price
        elif msg.field == 2:
            self.ask_price = msg.price
        elif msg.field == 4:
            self.last_prices.loc[dt.datetime.now()] = msg.price
            resampled_prices = \
                self.last_prices.resample(self.resample_interval,
                                          how='last',
                                          fill_method="ffill")
            self.average_price = resampled_prices.tail(
                self.averaging_period).mean()[0]

        self.perform_trade_logic()

    def perform_trade_logic(self):
        # Is buying at the market lower than the average price?
        is_buy_signal = self.ask_price < self.average_price

        # Is selling at the market higher than the average price?
        is_sell_signal = self.bid_price > self.average_price

        # Print signal values on every tick
        print dt.datetime.now(), \
            " BUY/SELL? ", is_buy_signal, "/", is_sell_signal, \
            " Avg:", self.average_price

        # Use generated signals, if any, to open a position
        if self.average_price != 0 \
            and self.bid_price != 0 \
            and self.ask_price != 0 \
            and self.position == 0 \
                and not self.is_position_opened:

            if is_sell_signal:
                self.place_market_order(self.symbol, self.qty, False)
                self.is_position_opened = True

            elif is_buy_signal:
                self.place_market_order(self.symbol, self.qty, True)
                self.is_position_opened = True

        # If position is already opened, use generated signals
        # to close the position.
        elif self.is_position_opened:

            if self.position > 0 and is_sell_signal:
                self.place_market_order(self.symbol, self.qty, False)
                self.is_position_opened = False

            elif self.position <0 and is_buy_signal:
                self.place_market_order(self.symbol, self.qty, True)
                self.is_position_opened = False

            # When the position is open, keep track of our
            # unrealized and realized P&Ls
            self.monitor_position()

    def monitor_position(self):
        print 'Position:%s UPnL:%s RPnL:%s' % (self.position,
                                               self.unrealized_pnl,
                                               self.realized_pnl)

    def place_market_order(self, symbol, qty, is_buy):
        contract = self.create_contract(symbol,
                                        'STK',
                                        'SMART',
                                        'SMART',
                                        'USD')
        buysell = 'BUY' if is_buy else 'SELL'
        order = self.create_order('MKT', qty, buysell)
        self.tws_conn.placeOrder(self.order_id, contract, order)
        self.order_id += 1

        print "Placed order", qty, "of", symbol, "to", buysell

    def create_contract(self, symbol, sec_type, exch, prim_exch, curr):
        contract = Contract()
        contract.m_symbol = symbol
        contract.m_secType = sec_type
        contract.m_exchange = exch
        contract.m_primaryExch = prim_exch
        contract.m_currency = curr
        return contract

    def create_order(self, order_type, quantity, action):
        order = Order()
        order.m_orderType = order_type
        order.m_totalQuantity = quantity
        order.m_action = action
        return order

    def request_market_data(self, symbol_id, symbol):
        contract = self.create_contract(symbol,
                                        'STK',
                                        'SMART',
                                        'SMART',
                                        'USD')
        self.tws_conn.reqMktData(symbol_id, contract, '', False)
        time.sleep(1)

    def cancel_market_data(self, symbol):
        self.tws_conn.cancelMktData(symbol)
        time.sleep(1)

    def request_account_updates(self, account_code):
        self.tws_conn.reqAccountUpdates(True, account_code)

    def connect_to_tws(self):
        self.tws_conn = Connection.create(port=self.port,
                                          clientId=self.client_id)
        self.tws_conn.connect()

    def disconnect_from_tws(self):
        if self.tws_conn is not None:
            self.tws_conn.disconnect()

    def register_callback_functions(self):
        # Assign server messages handling function.
        self.tws_conn.registerAll(self.server_handler)

        # Assign error handling function.
        self.tws_conn.register(self.error_handler, 'Error')

        # Register market data events.
        self.tws_conn.register(self.tick_event,
                               message.tickPrice,
                               message.tickSize)

    def start(self):
        try:
            self.connect_to_tws()
            self.register_callback_functions()
            self.request_market_data(self.symbol_id, self.symbol)
            self.request_account_updates(self.account_code)

            while True:
                time.sleep(1)

        except Exception, e:
            print "Error:", e
            self.cancel_market_data(self.symbol)

        finally:
            print "disconnected"
            self.disconnect_from_tws()

if __name__ == "__main__":
    system = AlgoSystem("FB", 100, "30s", 5)
    system.start()