from lib.common import constants
from lib.services import service


class PortfolioService(service.Service):

    def get_portfolios(self):
        return self.get(constants.urls.portfolio_search)

    def get_portfolio(self, portfolio_id):
        return self.get(f'{constants.urls.portfolio}', {'id': portfolio_id})

    def create_portfolio(self, portfolio_request):
        return self.post(constants.urls.portfolio, portfolio_request)

    def update_portfolio(self, portfolio_request):
        return self.put(constants.urls.portfolio, portfolio_request)

    def contribute_portfolio(self, contribution_request):
        return self.post(constants.urls.contribute, contribution_request)

    def follow_portfolio(self, portfolio_id):
        return self.put(f'{constants.urls.follow}', None,{'id': portfolio_id})

    def unfollow_portfolio(self, portfolio_id):
        return self.delete(f'{constants.urls.unfollow}', params={'id': portfolio_id})

    def get_portfolio_members(self, portfolio_id):
        return self.get(f'{constants.urls.members}', params={'portfolioId': portfolio_id})

    def delete_portfolio(self, portfolio_request):
        return self.delete(constants.urls.portfolio, portfolio_request)