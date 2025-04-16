from lib.common.logger import Logger
from lib.database import mysqldb

logger = Logger('dao.portfolio')

class PortfolioDao:

    def __init__(self):
        self.mysql_client = mysqldb.MySQLClient()
        self.mysql_client.connect()

    def get_portfolios_for_user(self, user_id):
        query = f"""
            SELECT
                portfolio.id,
                portfolio.name portfolio_name,
                portfolio.description portfolio_description,
                portfolio.max_members portfolio_max_members,
                portfolio.minimum_deposit portfolio_minimum_deposit,
                portfolio.followers portfolio_followers,
                portfolio.members portfolio_members,
                portfolio.created_at portfolio_created_at,
                portfolio.change_7d portfolio_change_7d,
                portfolio.change_30d portfolio_change_30d,
                portfolio.change_365d portfolio_change_365d,
                portfolio_follower.user_id portfolio_follower_user_id,
                portfolio_member.user_id portfolio_member_user_id,
                user.username portfolio_owner_name
            FROM
                portfolio
            INNER JOIN user ON user.id = portfolio.user_id
            LEFT JOIN portfolio_follower ON portfolio_follower.portfolio_id = portfolio.id AND portfolio_follower.user_id = {user_id}
            LEFT JOIN portfolio_member ON portfolio_member.portfolio_id = portfolio.id AND portfolio_member.user_id = {user_id}
        """

        return self.mysql_client.query(query)

    def get_portfolio_by_id(self, portfolio_id, user_id):
        query = f"""
            SELECT
                portfolio.id,
                portfolio.name portfolio_name,
                portfolio.description portfolio_description,
                portfolio.max_members portfolio_max_members,
                portfolio.minimum_deposit portfolio_minimum_deposit,
                portfolio.followers portfolio_followers,
                portfolio.members portfolio_members,
                portfolio.created_at portfolio_created_at,
                portfolio.change_7d portfolio_change_7d,
                portfolio.change_30d portfolio_change_30d,
                portfolio.change_365d portfolio_change_365d,
                portfolio_balance.cash portfolio_cash_balance,
                portfolio_balance.equity portfolio_equity_balance,
                portfolio_follower.user_id portfolio_follower_user_id,
                portfolio_member.user_id portfolio_member_user_id,
                user.id portfolio_owner_id,
                user.username portfolio_owner_name

                (SELECT COUNT(portfolio_stock.id) FROM portfolio_stock WHERE portfolio_stock.portfolio_id = {portfolio_id}) portfolio_total_stocks
            FROM
                portfolio
            INNER JOIN portfolio_balance ON portfolio_balance.portfolio_id = portfolio.id
            INNER JOIN user ON user.id = portfolio.user_id
            LEFT JOIN portfolio_follower ON portfolio_follower.portfolio_id = portfolio.id AND portfolio_follower.user_id = {user_id}
            LEFT JOIN portfolio_member ON portfolio_member.portfolio_id = portfolio.id AND portfolio_member.user_id = {user_id}
            
            WHERE portfolio.id = {portfolio_id}
        """

        return self.mysql_client.query(query)
