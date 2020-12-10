import requests
import os


class AlphaVantage:
    def __init__(self, api_key: str):
        self.API_KEY = api_key
        self.API_URL = "https://www.alphavantage.co/query"
        if not os.path.exists('stock_dfs'):
            os.makedirs('stock_dfs')

    # accepted interval 1min, 5min, 15min, 30min, 60min
    def get_monthly(self, symbol: str, interval='15min', duration=1):
        if os.path.exists(f'{symbol}.csv'):
            os.remove(f'{symbol}.csv')

        params = {"function": "TIME_SERIES_INTRADAY_EXTENDED",
                  "symbol": symbol,
                  "interval": interval,
                  "slice": '',
                  "apikey": "TGESH0A2UGSNU4WB"}

        for d in range(1, duration):
            _slice = f"year{2 if d // 12 else 1}month{d % 12}"
            params['slice'] = _slice

            response = requests.get(self.API_URL, params)

            with open(f'stock_dfs/{symbol}.csv', 'ab') as f:
                f.write(response.content)
        else:
            _slice = f"year{2 if duration // 12 else 1}month{duration % 12}"
            params['slice'] = _slice

            response = requests.get(self.API_URL, params)

            with open(f'stock_dfs/{symbol}.csv', 'ab') as f:
                f.write(response.content)
        print('Done')
