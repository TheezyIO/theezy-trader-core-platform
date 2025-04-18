from lib.common import constants
from lib.services import service

import os


class PolygonService(service.Service):

    def __init__(self):
        super().__init__('Bearer ' + os.getenv('POLYGON_API_KEY'), constants.urls.polygon)

    def get_stock_quotes(self, stock_ticker, date):
        return self.get(f'{constants.urls.stock_quotes}{stock_ticker}', {'timestamp': date, 'order': 'desc', 'limit': 5})

    def get_stock_historical_data(self, stock_ticker, from_date, to_date):
        return self.get(constants.urls.stock_daily_aggregates.format(stock_ticker, from_date, to_date))

    def search_stocks(self, search_term=None, cursor=None):
        params = {'market': 'stocks'}
        if search_term:
            gte = search_term.upper()
            params['ticker.gte'] = gte
            params['ticker.lt'] = chr(ord(gte[0]) + 1)

        if cursor:
            params['cursor'] = cursor
        else:
            params['limit'] = '10'

        return self.get(constants.urls.stock_tickers, params)

    def get_stock_snapshots(self, stock_tickers):
        params = {'tickers': ','.join(stock_tickers)}
        return self.get(constants.urls.stock_ticker_snapshots, params)
