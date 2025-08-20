from lib.common.logger import Logger
from lib.database import mysqldb

logger = Logger('dao.stock')

class StockDao:

    def __init__(self):
        self.mysql_client = mysqldb.MySQLClient()
        self.mysql_client.connect()

    def get_stocks_by_earliest_date(self):
        query = """
            SELECT
                stock.id stock_id,
                stock.name stock_name,
                stock.ticker stock_ticker,

                MIN(portfolio_stock.created_at) earliest_event_date
            FROM
                portfolio_stock, stock, stock_daily_price
            WHERE
                portfolio_stock.stock_id = stock.id
            GROUP BY
                stock_name, stock_ticker
        """

        return self.mysql_client.query(query)

    def get_stocks_in_portfolio(self, portfolio_id):
        query = f"""
            SELECT
                stock.id stock_id,
                stock.name stock_name,
                stock.ticker stock_ticker,
                portfolio_stock.id portfolio_stock_id,
                portfolio_stock.average_price portfolio_stock_average_price,
                portfolio_stock.amount portfolio_stock_amount
            FROM
                stock, portfolio_stock
            WHERE
                stock.id = portfolio_stock.stock_id AND portfolio_stock.portfolio_id = {portfolio_id}
        """

        return self.mysql_client.query(query)

    # Optimize this query to use BETWEEN instead of listing all dates
    def get_daily_prices_by_dates(self, stock_ticker, from_date, to_date):
        query = f"""
            SELECT
                stock.id stock_id, 
                stock.ticker stock_ticker,
                stock.name stock_name,
                stock_daily_price.price stock_daily_price,
                stock_daily_price.event_date stock_price_event_date
            FROM
                stock_daily_price, stock
            WHERE
                stock.id = stock_daily_price.stock_id AND stock.ticker = '{stock_ticker}'
                AND stock_daily_price.event_date BETWEEN '{from_date}' AND '{to_date}'
        """

        return self.mysql_client.query(query)

    def get_portfolio_stock_details(self, portfolio_id, stock_ticker, user_id=None):
        query = f"""
            SELECT
                stock.id stock_id,
                stock.name stock_name,
                stock.ticker stock_ticker,
                
                stock_cache.id stock_cache_id,
                stock_cache.name stock_cache_name,
                stock_cache.ticker stock_cache_ticker,
                
                portfolio.id portfolio_id,
                portfolio_stock.id portfolio_stock_id,
                portfolio_stock.amount portfolio_stock_amount,
                portfolio_stock.average_price portfolio_stock_average_price,
                portfolio_stock.created_at portfolio_stock_created_at,
                
                portfolio_balance.id portfolio_balance_id,
                portfolio_balance.cash portfolio_cash_balance,
                portfolio_balance.equity portfolio_equity_balance,
                
                user.id user_id,
                user.name user_name,
                
                account_balance.id account_balance_id,
                account_balance.cash account_cash_balance,
                account_balance.equity account_equity_balance
            FROM
                user
            INNER JOIN portfolio ON user.id = portfolio.user_id
            INNER JOIN portfolio_balance ON portfolio.id = portfolio_balance.portfolio_id
            INNER JOIN account_balance ON user.id = account_balance.user_id
            LEFT JOIN stock stock_cache ON stock_cache.ticker = '{stock_ticker}'
            LEFT JOIN portfolio_stock ON portfolio.id = portfolio_stock.portfolio_id AND portfolio_stock.stock_id = (
                SELECT stock.id FROM stock, portfolio_stock WHERE stock.id = portfolio_stock.stock_id AND stock.ticker = '{stock_ticker}' AND portfolio_stock.portfolio_id = {portfolio_id}
            )
            LEFT JOIN stock ON portfolio_stock.stock_id = stock.id AND stock.ticker = '{stock_ticker}'
            WHERE portfolio.id = {portfolio_id} {"AND user.id = '" + user_id + "'" if user_id else ""}
        """
        return self.mysql_client.query(query)

    def get_portfolio_stock_transactions(self, portfolio_stock_id):
        query = f"""
            SELECT
                stock.id stock_id,
                stock.name stock_name,
                stock.ticker stock_ticker,
                portfolio_stock.id portfolio_stock_id,
                portfolio_stock_transaction.amount portfolio_stock_transaction_amount,
                portfolio_stock_transaction.price portfolio_stock_transaction_price,
                portfolio_stock_transaction.event_time portfolio_stock_transaction_event_time,
                transaction_type.name transaction_type_name
            FROM
                stock, portfolio_stock, portfolio_stock_transaction, transaction_type
            WHERE
                stock.id = portfolio_stock.stock_id AND portfolio_stock.id = portfolio_stock_transaction.portfolio_stock_id AND
                portfolio_stock_transaction.transaction_type_id = transaction_type.id AND portfolio_stock.id = {portfolio_stock_id}
        """
        return self.mysql_client.query(query)

    def create_transaction(self, transaction):
        self.mysql_client.insert('portfolio_stock_transaction', [transaction])

    def update_portfolio_stock(self, portfolio_stock_update, portfolio_stock_id):
        self.mysql_client.update('portfolio_stock', portfolio_stock_update, f'id={portfolio_stock_id}')

    def update_daily_prices_for_ticker(self, daily_prices):
        self.mysql_client.insert('stock_daily_price', daily_prices)
