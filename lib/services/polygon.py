from lib.common import constants
from lib.services import service

import os


class PolygonService(service.Service):

    def __init__(self):
        super().__init__('Bearer ' + os.getenv('POLYGON_API_KEY'), constants.urls.polygon)

    def get_stock_quotes(self, stock_ticker, date):
        return self.get(f'{constants.urls.stock_quotes}{stock_ticker}', {'timestamp': date, 'order': 'desc', 'limit': 5})
