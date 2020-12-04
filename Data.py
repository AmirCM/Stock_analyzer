import json
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import mplfinance as mpf
import matplotlib.dates as mdates
import pandas_datareader.data as web
import requests
import pickle
import bs4 as bs
import os
import pandas as pd
from alpha_vantage.timeseries import TimeSeries


def save_sp500_tickers():
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker)

    print(len(tickers), tickers)
    with open("sp500tickers.pickle", "wb") as f:
        pickle.dump(tickers, f)
    return tickers


def get_data_from_yahoo(reload_sp500=False):
    if reload_sp500:
        tickers = save_sp500_tickers()
    else:
        with open("sp500tickers.pickle", "rb") as f:
            tickers = pickle.load(f)
    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')

    start = dt.datetime(2010, 1, 1)
    end = dt.datetime.now()
    ts = TimeSeries(key='TGESH0A2UGSNU4WB', output_format='pandas', indexing_type='date')
    for ticker in tickers[:10]:
        # just in case your connection breaks, we'd like to save our progress!
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            df, _ = ts.get_daily(symbol=ticker, outputsize='full')
            df = df.drop("Symbol", axis=1)
            df.to_csv('stock_dfs/{}.csv'.format(ticker))
        else:
            print('Already have {}'.format(ticker))


def compile_data():
    with open("sp500tickers.pickle", "rb") as f:
        tickers = pickle.load(f)

    main_df = pd.DataFrame()

    for count, ticker in enumerate(tickers):
        df = pd.read_csv('stock_dfs/{}.csv'.format(ticker))
        df.set_index('Date', inplace=True)

        df.rename(columns={'Adj Close': ticker}, inplace=True)
        df.drop(['Open', 'High', 'Low', 'Close', 'Volume'], 1, inplace=True)

        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df, how='outer')

        if count % 10 == 0:
            print(count)
    print(main_df.head())
    main_df.to_csv('sp500_joined_closes.csv')


def visualize_data():
    df = pd.read_csv('sp500_joined_closes.csv')
    df['AAPL'].plot()
    plt.show()


API_URL = "https://www.alphavantage.co/query"
symbol = 'MMM'

data = {"function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "outputsize": "composite",
        "datatype": "json",
        "apikey": "TGESH0A2UGSNU4WB"}

response = requests.get(API_URL, data)
response_json = response.json()  # maybe redundant

data = pd.DataFrame.from_dict(response_json['Time Series (Daily)'], orient='index').sort_index(axis=1)
data = data.rename(columns={'1. open': 'Open', '2. high': 'High', '3. low': 'Low', '4. close': 'Close',
                            '5. volume': 'Volume'})
data = data[['Open', 'High', 'Low', 'Close', 'Volume']]
print(data.tail())

"""get_data_from_yahoo()
compile_data()
visualize_data()"""
