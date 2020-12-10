import bitfinex
import pandas as pd
import numpy as np
import datetime
import time
import mplfinance as mpf
import sys
import matplotlib.pyplot as plt


def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '█' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()


def fetch_data(start, stop, symbol, interval=1):
    api_v2 = bitfinex.bitfinex_v2.api_v2()
    print('From {} to {} for {}'.format(pd.to_datetime(start, unit='ms'),
                                        pd.to_datetime(stop, unit='ms'), symbol))
    sec = (stop - start) // 1000
    min = sec // 60
    k = int((min // interval) // 1000 + 1)
    step = interval * 60 * 1000000

    data = []
    interval = str(interval) + 'm'

    for i in range(k):
        progress(i, k, status='Fetching data')
        if start + step < stop:
            res = api_v2.candles(symbol=symbol, interval=interval, limit=1000, start=start, end=start + step)
            data.extend(res)
            start += step
        else:
            res = api_v2.candles(symbol=symbol, interval=interval, limit=1000, start=start, end=stop)
            data.extend(res)
        time.sleep(1.5)
    progress(k, k, status='Fetching Done')
    print('Fetching Done')
    ind = [np.ndim(x) != 0 for x in data]
    data = [i for (i, v) in zip(data, ind) if v]
    return data


df_old = pd.read_csv('BTCUSD.csv', parse_dates=True, index_col='time', )

pair = 'BTCUSD'
bin_size = 30

t_start = datetime.datetime(2020, 9, 10, 0, 0)
t_start = time.mktime(t_start.timetuple()) * 1000

t_stop = datetime.datetime.now()
t_stop = time.mktime(t_stop.timetuple()) * 1000

# api_v1 = bitfinex.bitfinex_v1.api_v1()
pair_data = fetch_data(start=t_start, stop=t_stop, symbol=pair, interval=bin_size)

names = ['time', 'open', 'close', 'high', 'low', 'volume']
df = pd.DataFrame(pair_data, columns=names)
df.drop_duplicates(inplace=True)
df.set_index('time', inplace=True)
df.sort_index(inplace=True)
df.index = pd.to_datetime(df.index, unit='ms')

mpf.plot(df_old, type='candle', title='New BTC/USD', volume=True, style='yahoo')
mpf.plot(df_old, type='candle', title='BTC/USD', volume=True, style='yahoo')

print(df.tail())
print(df_old.tail())
"""
# Append the new data to the old data set
df_old = df_old.append(df)

# Remove duplicates and sort the data
df_old.drop_duplicates(inplace=True)
df_old.sort_index(inplace=True)

df.to_csv('BTCUSD.csv')

fig, ax = plt.subplots(1, 1, figsize=(18, 5))

ax.plot(df['close'])
ax.set_xlabel('date', fontsize=16)
ax.set_ylabel('BTC price [USD]', fontsize=16)
ax.set_title('Bitcoin closing price from {} to {}'.format(df.index[0], df.index[-1]))
ax.grid()

plt.show()
"""
