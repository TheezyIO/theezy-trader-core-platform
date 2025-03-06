from lib.common import constants
from lib.services import service


class PortfolioService(service.Service):

    def get_portfolios(self):
        return self.get(constants.urls.portfolio)

    def get_portfolio(self, portfolio_id):
        return super().get(f'{constants.urls.portfolio}', {'id': portfolio_id})

    def create_portfolio(self, portfolio_request):
        return super().post(constants.urls.portfolio, portfolio_request)

    def update_portfolio(self, portfolio_request):
        return super().put(constants.urls.portfolio, portfolio_request)

    def contribute_portfolio(self, contribution_request):
        return super().post(constants.urls.contribute, contribution_request)

    def follow_portfolio(self, portfolio_id):
        return super().put(f'{constants.urls.follow}', None,{'id': portfolio_id})

    def unfollow_portfolio(self, portfolio_id):
        return super().delete(f'{constants.urls.unfollow}', params={'id': portfolio_id})

    def get_portfolio_members(self, portfolio_id):
        return self.get(f'{constants.urls.members}', params={'id': portfolio_id})
