from lib.common import constants
from lib.services import service


class AccountService(service.Service):

    def deposit_funds(self, deposit_amount):
        return self.post(constants.urls.account_deposit, {'amount': deposit_amount})

    def get_balance(self):
        return self.get(constants.urls.account_balance)
