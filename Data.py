import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web

style.use('ggplot')

# Get online data
"""start = dt.datetime(2019, 1, 1)
end = dt.datetime(2020, 12, 1)

df = web.DataReader('TSLA', 'yahoo', start, end)
df.to_csv('TSLA.csv')
print(df.head())"""

df = pd.read_csv('TSLA.csv', parse_dates=True, index_col=0)
df['ma'] = df['Adj Close'].rolling(window=100, min_periods=0).mean()
# df.dropna(inplace=True)

row1 = plt.subplot2grid((6, 1), (0, 0), rowspan=5, colspan=1)
row2 = plt.subplot2grid((6, 1), (5, 0), rowspan=1, colspan=1, sharex=row1)

row1.plot(df.index, df['Adj Close'], color='b')
row1.plot(df.index, df['ma'], color='g')
row2.bar(df.index, df['Volume'], color='b')
plt.show()
