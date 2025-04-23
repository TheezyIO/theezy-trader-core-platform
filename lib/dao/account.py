from lib.common.logger import Logger
from lib.database import mysqldb

logger = Logger('dao.account')

class AccountDao:

    def __init__(self):
        self.mysql_client = mysqldb.MySQLClient()
        self.mysql_client.connect()
    
    def get_account_for_user(self, user_id):
        query = f"""
            SELECT 
                user.id userId, 
                user.username, 
                account_balance.id, 
                account_balance.cash,
                account_balance.equity,
                account_balance.modified_at
            FROM 
                user, account_balance 
            WHERE
                user.id = account_balance.user_id AND user.id = '{user_id}'
        """
        
        return self.mysql_client.query(query)

    def create_account(self, user_id):
        account_balance_data = {'cash': 0, 'equity': 0, 'user_id': user_id}
        self.mysql_client.insert('account_balance', [account_balance_data])
    
    def create_transaction(self, transaction):
        self.mysql_client.insert('account_balance_transaction', [transaction])
        
    def update_account(self, account_update, account_id):
        self.mysql_client.update('account_balance', {account_update}, f'id={account_id}')