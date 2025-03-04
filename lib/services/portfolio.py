from lib.common import constants
from lib.services import service


class PortfolioService(service.Service):

    def __init__(self, authorization_token):
        super().__init__(authorization_token)

    def get(self, url, params=None):
        return super().get(url, params)

    def post(self, url, body, params=None):
        return super().post(url, body, params)

    def put(self, url, body, params=None):
        return super().put(url, body, params)

    def get_portfolios(self):
        return self.get(constants.urls.portfolio)

    def get_portfolio(self, portfolio_id):
        return self.get(f'{constants.urls.portfolio}', {'id': portfolio_id})

    def create_portfolio(self, portfolio_request):
        return self.post(constants.urls.portfolio, portfolio_request)

    def update_portfolio(self, portfolio_request):
        return self.put(constants.urls.portfolio, portfolio_request)

    def contribute_portfolio(self, contribution_request):
        return self.post(constants.urls.contribute, contribution_request)
