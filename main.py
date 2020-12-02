from binance.client import Client
from binance.websockets import BinanceSocketManager

api_key = '1TWHLJCTidI6ki4SAiBsEQRNBQYkSmTkRzcMCAyHQeWOewLiJsSAsyX3XO2TJikn'
api_secret = 'BMBtKYMDhw3QM5N5En9CHyyN8UcGvmfBkew6YRcLKlQOLxGiKsASRVeHBqO3nA3X'
client = Client(api_key, api_secret)

# get market depth
depth = client.get_order_book(symbol='BTCUSDT')

# get all symbol prices
# prices = client.get_all_tickers()
prices = client.get_orderbook_ticker(symbol='BTCUSDT')
print(prices)

"""
# start aggregated trade websocket for BNBBTC
def process_message(msg):
    print("message type: {}".format(msg['e']))
    print(msg)
    # do something


bm = BinanceSocketManager(client)
bm.start_aggtrade_socket('BTCUSDT', process_message)
bm.start()"""

# get historical kline data from any date range

# fetch 1 minute klines for the last day up until now
klines = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1HOUR, "1 day ago UTC")
print(len(klines))
for each in klines:
    print(each)
# fetch 30 minute klines for the last month of 2017
#klines = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_30MINUTE, "1 Dec, 2017", "1 Jan, 2018")

# fetch weekly klines since it listed
#klines = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1MONTH, "1 Jan, 2020")
#print(len(klines), klines)
