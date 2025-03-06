from lib.common import constants
from lib.services import service


class StockService(service.Service):

    def get_details(self, stock_id):
        self.get(f'{constants.urls.stock_details}', {'id': stock_id})
