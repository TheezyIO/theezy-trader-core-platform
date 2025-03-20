from lib.common.logger import Logger
from lib.services import polygon
from lib.dao.stock import StockDao
from datetime import datetime, timedelta


logger = Logger('stock.dailyprice')

def main():
    logger.info(f'Function invocation started...')

    stock_dao = StockDao()
    stocks_by_earliest_date = stock_dao.get_stocks_by_earliest_date()

    for stock in stocks_by_earliest_date:
        date_filter_set = set()
        target_date = datetime.date(datetime.now())
        current_date = datetime.date(stock['earliest_event_date'])

        while current_date < target_date:
            if current_date.strftime('%A') not in ['Saturday', 'Sunday']:
                date_filter_set.add(current_date.isoformat())
            current_date += timedelta(days=1)

        # Further optimize this by sending queries for multiple stock tickers for multiple date ranges at once
        existing_price_dates = stock_dao.get_daily_prices_by_dates(stock['stock_ticker'], list(date_filter_set))

        for existing_daily_date in existing_price_dates:
            iso_format = existing_daily_date['stock_price_event_date'].isoformat()
            date_filter_set.remove(iso_format)

        missing_price_dates = list(date_filter_set)
        logger.info(f'Missing price dates for {stock["stock_ticker"]} {missing_price_dates}')

        polygon_service = polygon.PolygonService()

        daily_prices = []
        for missing_date in missing_price_dates:
            # Is there a way to get daily aggregations that doesn't necessitate sending one request per ticker per day to polygon
            quotes_data = polygon_service.get_stock_quotes(stock['stock_ticker'], missing_date)
            if result := quotes_data['results'][0] if 'results' in quotes_data and len(quotes_data['results']) else None:
                daily_prices.append({
                    'stock_id': stock['stock_id'],
                    'event_date': missing_date,
                    'price': int(round(result['bid_price'] * 100))
                })

        stock_dao.update_daily_prices_for_ticker(daily_prices)
        logger.info(f'{len(daily_prices)} daily updates were added for {stock["stock_ticker"]}')

    return 'Stock Daily Price update has completed successfully'
