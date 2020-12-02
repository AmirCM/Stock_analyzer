import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import mplfinance as mpf
import matplotlib.dates as mdates
import pandas as pd
import pandas_datareader.data as web
from mplfinance.original_flavor import volume_overlay

style.use('ggplot')

df = pd.read_csv('TSLA.csv', parse_dates=True, index_col=0)

df_ohlc = df['Adj Close'].resample('10D').ohlc()
df_volume = df['Volume'].resample('10D').sum()
df_ohlc['volume'] = df_volume

mpf.plot(df_ohlc, type='candle', title='TSLA STOCK', volume=True, style='yahoo')
