from lib.common import constants
from lib.services import service


class PortfolioService(service.Service):

    def __init__(self, authorization_token):
        super().__init__(authorization_token)

    def get(self, url):
        return super().get(url)

    def get_portfolios(self):
        return self.get(constants.urls.portfolio)
