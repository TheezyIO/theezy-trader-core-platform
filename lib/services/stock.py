from lib.common import constants
from lib.services import service


class StockService(service.Service):

    def get_details(self, stock_ticker, portfolio_id=None):
        return self.get(f'{constants.urls.stock_details}', {'ticker': stock_ticker, 'portfolioId': portfolio_id})

    def search(self, portfolio_id):
        return self.get(f'{constants.urls.stock_search}', {'portfolioId': portfolio_id})

    def get_transactions(self, stock_id):
        return self.get(f'{constants.urls.transactions}', {'id': stock_id, 'scope': 'PORTFOLIO_STOCK'})
