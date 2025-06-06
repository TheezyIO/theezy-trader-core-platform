from lib.common import constants
from lib.services import service


class StockService(service.Service):

    def get_details(self, stock_ticker, portfolio_id=None):
        return self.get(f'{constants.urls.stock_details}', {'ticker': stock_ticker, 'portfolioId': portfolio_id})

    def search(self, **kwargs):
        return self.get(
            f'{constants.urls.stock_search}', {
                'portfolioId': kwargs.get('portfolio_id'),
                'search': kwargs.get('search'),
                'cursor': kwargs.get('cursor')
            })

    def get_portfolio_stocks(self, portfolio_id):
        return self.get(f'{constants.urls.stock_by_portfolio}', {'portfolioId': portfolio_id})

    def get_transactions(self, stock_id):
        return self.get(f'{constants.urls.transactions}', {'id': stock_id, 'scope': 'PORTFOLIO_STOCK'})

    def purchase(self, purchase_request):
        return self.post(constants.urls.stock_purchase, purchase_request)

    def sell(self, sell_request):
        return self.post(constants.urls.stock_sell, sell_request)
