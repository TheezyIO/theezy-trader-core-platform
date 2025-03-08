from lib.common import constants
from lib.services import service


class StockService(service.Service):

    def get_details(self, stock_id):
        return self.get(f'{constants.urls.stock_details}', {'id': stock_id})

    def search(self, portfolio_id):
        return self.get(f'{constants.urls.stock_search}', {'portfolioId': portfolio_id})
