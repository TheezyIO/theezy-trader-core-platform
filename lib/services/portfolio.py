from lib.common import constants
from lib.services import service


class PortfolioService(service.Service):

    def __init__(self, authorization_token):
        super().__init__(authorization_token)

    def get(self, url, params=None):
        return super().get(url, params)

    def get_portfolios(self):
        return self.get(constants.urls.portfolio)

    def get_portfolio(self, portfolio_id):
        return self.get(f'{constants.urls.portfolio}', {'id': portfolio_id})

