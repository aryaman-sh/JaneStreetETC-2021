#!/usr/bin/python3
from __future__ import print_function

import sys
import socket
import json

# ~~~~~============== CONFIGURATION  ==============~~~~~
""" REMOVED """
# ~~~~~============== NETWORKING CODE ==============~~~~~
def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((exchange_hostname, port))
    return s.makefile("rw", 1)


def write_to_exchange(exchange, obj):
    json.dump(obj, exchange)
    exchange.write("\n")


def read_from_exchange(exchange):
    return json.loads(exchange.readline())


# ~~~~~============== MAIN LOOP ==============~~~~~
bond_prices = []

def collect_price(exchange):
    c = 0
    days_to_save = 30
    print("saving data")
    while (c < days_to_save):
        data = read_from_exchange(exchange)
        type = data["type"];
        if type == "trade":
            if (data["symbol"] == "BOND"):
                bond_prices.append(data["price"])

        time.sleep(0.01)
        count += 1

order_id = 0

def bonds_order_manager(exchange, price, qty, action):
    global order_id
    if action == 0:
        order_id += 1
        write_to_exchange(exchange,
                          {"type": "add", "order_id": order_id, "symbol": "BOND", "dir": "BUY", "price": price,
                           "size": qty})
    if action == 1:
        order_id += 1
        write_to_exchange(exchange,
                          {"type": "add", "order_id": order_id, "symbol": "BOND", "dir": "SELL", "price": price,
                           "size": qty})

def bond_strat(exchange, buy_ord, sell_ord):
    for i in range(len(buy_ord)):
        if int(buy_ord[i][0]) > 1000:
            print("selling")
            bonds_order_manager(exchange, buy_ord[i][0], buy_ord[i][1], 1)
    for i in range(len(sell_ord)):
        if int(sell_ord[i][0]) < 1000:
            print("buying")
            bonds_order_manager(exchange, sell_ord[i][0], sell_ord[i][1], 0)

def xlf_manager(exchange, price, qty, action, symbol, typeval):
    global order_id
    if action == 0:
        order_id += 1
        write_to_exchange(exchange,
                          {"type": typeval, "order_id": order_id, "symbol": symbol, "dir": "BUY", "price": price,
                           "size": qty})
    if action == 1:
        order_id += 1
        write_to_exchange(exchange,
                          {"type": typeval, "order_id": order_id, "symbol": symbol, "dir": "SELL", "price": price,
                           "size": qty})

def xlf_strat(exchange, gs, ms, wfc, xlf):
    def _calc_xlf_value(gs, ms, wfc, direction):
        return 3 * 1000 + 2 * gs[direction][0][0] + 3 * ms[direction][0][0] + 2 * wfc[direction][0][0]

    def _execute_basket_items(gs, ms, wfc, direction):
        reverse_direction = 0 if direction == 1 else 1
        xlf_manager(exchange, gs[reverse_direction][0][0], 2, direction, 'GS', 'ADD')
        xlf_manager(exchange, ms[reverse_direction][0][0], 3, direction, 'MS', 'ADD')
        xlf_manager(exchange, wfc[reverse_direction][0][0], 2, direction, 'WFC', 'ADD')

    if _calc_xlf_value(gs, ms, wfc, 0) + 102 < (xlf[0][0][0] * 10):
        _execute_basket_items(gs, ms, wfc, 0)
        xlf_manager(exchange, xlf[0][0][0], 10, 0, 'XLF', 'CONVERT')
        xlf_manager(exchange, xlf[0][0][0], 10, 1, 'XLF', 'ADD')

    elif _calc_xlf_value(gs, ms, wfc, 0) > (xlf[1][0][0] * 10 + 102):
        xlf_manager(exchange, xlf[1][0][0], 10, 0, 'XLF', 'ADD')
        xlf_manager(exchange, xlf[1][0][0], 10, 1, 'XLF', 'CONVERT')

def collect_price(exchange):
    c = 0
    days_to_save = 30
    print("saving data")
    while(c < days_to_save):
        data = read_from_exchange(exchange)
        type = data["type"];
        if type=="trade":
            data["symbol"]
            bond_prices.append(data["price"])
        time.sleep(0.01)
        count += 1

def calculate_xlf_fair_price(past_transactions):
    try:
        xlf_fair_value = 0.3 * past_transactions['BOND'][0] + 0.2 * past_transactions['GS'][0] + 0.3 * \
                         past_transactions['MS'][0] + 0.2 * past_transactions['WFC'][0]
    except Exception as e:
        print(e)
        return None
    return xlf_fair_value

def find_gradient(vector):
    changes = []
    for x in range(0, len(vector) - 1):
        changes.append(vector[x + 1] - vector[x])

    return sum(changes) / len(changes)

def main():
    exchange = connect()
    write_to_exchange(exchange, {"type": "hello", "team": team_name.upper()})
    hello_from_exchange = read_from_exchange(exchange)
    print("The exchange replied:", hello_from_exchange, file=sys.stderr)
    order_id = 0
    past_transactions = {}
    avg_prices = {}
    xlf_fair_values = [0, 0, 0, 0, 0]
    xlf_fair_gradient = 0
    gradient_treshold = 0.1
    while True:
        message = read_from_exchange(exchange)
        # print(avg_prices)
        if message['type'] == 'open':
            print("The round has begun")
            symbols = message['symbols']
            live_orders = {sym: {"buy": {}, "sell": {}} for sym in symbols}
            past_transactions = {sym: [0, 0, 0, 0, 0] for sym in symbols}
            avg_prices = {sym: 0 for sym in symbols}
        if message["type"] == "close":
            print("The round has ended")
        if message["type"] == "trade":
            past_transactions[message['symbol']].insert(0, message["price"])
            if len(past_transactions[message['symbol']]) > 5:
                past_transactions[message['symbol']] = past_transactions[message['symbol']][0:6]
            avg_prices[message['symbol']] = sum(past_transactions[message['symbol']]) / len(
                past_transactions[message['symbol']])
        if message["type"] == "BOND":
            pass  # print(message["price"])
        if message['type'] == "book":
            if message['symbol'] == 'XLF':
                buy = message['buy']
                sell = message['sell']
            if message['symbol'] == "VALE":
                buy_vale = message['buy']
                sell_vale = message['sell']
        if message['type'] == 'reject':
            print(message['error'])
        xlf_fair_values.insert(0, calculate_xlf_fair_price(past_transactions))
        if len(xlf_fair_values) > 5:
            xlf_fair_values = xlf_fair_values[0:6]
        if None in xlf_fair_values:
            continue
        # xlf_fair_gradient = find_gradient(xlf_fair_values)
        # xlf_real_gradient = find_gradient(past_transactions["XLF"])
        print("XLF FAIR: ", xlf_fair_values)
        print("XLF REAL: ", past_transactions["XLF"])
        if past_transactions['XLF'][0] - xlf_fair_values[0] < -15:
            write_to_exchange(exchange,
                              {"type": "add", "order_id": order_id, "symbol": "XLF", "dir": "BUY", "price": sell[0][0],
                               "size": 10})
            # live_orders['XLF']["buy"][order_id] = sell[0][0]
            order_id += 1

        if past_transactions['XLF'][0] - xlf_fair_values[0] > 15:
            write_to_exchange(exchange,
                              {"type": "add", "order_id": order_id, "symbol": "XLF", "dir": "SELL", "price": buy[0][0],
                               "size": 10})
            order_id += 1
            # live_orders['XLF']["sell"][order_id] = buy[0][0]

        if avg_prices["VALE"] - avg_prices['VALBZ'] < -20:
            write_to_exchange(exchange, {"type": "add", "order_id": order_id, "symbol": "VALE", "dir": "BUY",
                                         "price": sell_vale[0][0], "size": 1})
            order_id += 1

        if avg_prices["VALE"] - avg_prices['VALBZ'] > 20:
            write_to_exchange(exchange, {"type": "add", "order_id": order_id, "symbol": "VALE", "dir": "SELL",
                                         "price": buy_vale[0][0], "size": 1})
            order_id += 1

            """ Initial Bond code
            if message["type"] == "trade":
                if message["symbol"] == "BOND":
                    #print(message)
                    if (message["price"] > 1000):
    
                        order_id +=1
                        print("sell qty 10")
                        write_to_exchange(exchange, {"type" : "add", "order_id":order_id, "symbol" : "BOND", "dir" : "SELL", "price" :1001, "size":10})
                    if (message["price"] < 1000):
                        order_id += 1
                        print("buy qty 10")
                        write_to_exchange(exchange, {"type":"add","order_id":order_id,"symbol":"BOND", "dir": "BUY", "price":998,"size":10})
            """


if __name__ == "__main__":
    main()
