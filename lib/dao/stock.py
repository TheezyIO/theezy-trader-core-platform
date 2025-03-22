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

    # Optimize this query to use BETWEEN instead of listing all dates
    def get_daily_prices_by_dates(self, stock_ticker, dates):
        query = """
            SELECT
                stock.id stock_id, 
                stock.ticker stock_ticker,
                stock.name stock_name,
                stock_daily_price.event_date stock_price_event_date
            FROM
                stock_daily_price, stock
            WHERE
                stock.id = stock_daily_price.stock_id AND stock.ticker = '{}' AND stock_daily_price.event_date IN ({})
        """

        return self.mysql_client.query(query.format(stock_ticker, ', '.join(map(lambda date: "'%s'" % date, dates))))

    def update_daily_prices_for_ticker(self, daily_prices):
        self.mysql_client.insert('stock_daily_price', daily_prices)
