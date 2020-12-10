from AlphaVantage import AlphaVantage
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
        tickers.append(ticker[:len(ticker) - 1])

    with open("sp500tickers.pickle", "wb") as f:
        pickle.dump(tickers, f)
    return tickers


def get_data(reload_sp500=False):
    if reload_sp500:
        tickers = save_sp500_tickers()
    else:
        with open("sp500tickers.pickle", "rb") as f:
            tickers = pickle.load(f)
    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')

    ts = AlphaVantage('TGESH0A2UGSNU4WB')
    for ticker in tickers[:10]:
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            print('Getting have {}'.format(ticker))
            ts.get_monthly(symbol=ticker, interval='60min', duration=1)
        else:
            print('Already have {}'.format(ticker))


def compile_data():
    with open("sp500tickers.pickle", "rb") as f:
        tickers = pickle.load(f)

    main_df = pd.DataFrame()

    for count, ticker in enumerate(tickers[:10]):
        df = pd.read_csv('stock_dfs/{}.csv'.format(ticker))
        print(df.head())
        df.set_index('time', inplace=True)
        df.rename(columns={'close': ticker}, inplace=True)
        df.drop(['open', 'high', 'low', 'volume'], 1, inplace=True)
        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df, how='outer')

        if count % 10 == 0:
            print(count)
    print(main_df.head())
    main_df.to_csv('sp500_joined_closes.csv')


def visualize_data(stock: str):
    df = pd.read_csv(f'stock_dfs/Bitcoin_Historical_Data.csv', parse_dates=True, index_col=0)
    df.rename(
        columns={'Price': 'Close', 'Vol.': 'Volume'},
        inplace=True)
    print(df.shape)
    print(df.head())
    mpf.plot(df, type='candle', title=stock, volume=True, style='yahoo')


# get_data()
visualize_data('MMM')

