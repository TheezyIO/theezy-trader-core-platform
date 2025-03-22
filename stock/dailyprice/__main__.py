from lib.common.logger import Logger
from lib.services import polygon
from lib.dao import stock
from datetime import datetime, timedelta

logger = Logger('stock.dailyprice')

def main():
    logger.info(f'Function invocation started...')
    logger.info('Was able to successfully import mysql')

    stock_dao = stock.StockDao()
    stocks_by_earliest_date = stock_dao.get_stocks_by_earliest_date()
    for stock_data in stocks_by_earliest_date:
        date_filter_set = set()
        earliest_date = stock_data['earliest_event_date'].date()
        target_date = datetime.date(datetime.now())
        current_date = earliest_date

        while current_date < target_date:
            if current_date.strftime('%A') not in ['Saturday', 'Sunday']:
                date_filter_set.add(current_date.isoformat())
            current_date += timedelta(days=1)

        # Further optimize this by sending queries for multiple stock tickers for multiple date ranges at once
        existing_price_dates = stock_dao.get_daily_prices_by_dates(stock_data['stock_ticker'], earliest_date, target_date)

        for existing_daily_date in existing_price_dates:
            iso_format = existing_daily_date['stock_price_event_date'].isoformat()
            date_filter_set.remove(iso_format)

        missing_price_dates = sorted(list(date_filter_set))
        logger.info(f'Missing price dates for {stock_data["stock_ticker"]} {missing_price_dates}')

        polygon_service = polygon.PolygonService()

        daily_prices = []
        aggregates = []
        next_missing_date = None
        for missing_date in missing_price_dates:
            if not next_missing_date:
                aggregates.append([missing_date])
                next_missing_date = (datetime.strptime(missing_date, '%Y-%m-%d').date()) + timedelta(days=1)
            elif next_missing_date.isoformat() != missing_date:
                aggregates[-1].append(next_missing_date.isoformat())
                if aggregates[-1][0] != next_missing_date.isoformat():
                    aggregates.append([missing_date])
                next_missing_date = (datetime.strptime(missing_date, '%Y-%m-%d').date()) + timedelta(days=1)

        if next_missing_date and aggregates:
            aggregates[-1].append(next_missing_date.isoformat())

        for aggregate in aggregates:
            # Is there a way to get daily aggregations that doesn't necessitate sending one request per ticker per day to polygon
            if len(aggregate) > 1:
                quotes_data = polygon_service.get_stock_historical_data(stock_data['stock_ticker'], aggregate[0], aggregate[-1])
                if results := quotes_data['results'] if 'results' in quotes_data else None:
                    for result in results:
                        daily_prices.append({
                            'stock_id': stock_data['stock_id'],
                            'event_date': datetime.fromtimestamp(int(round(result['t'] / 1000))).strftime('%Y-%m-%d'),
                            'price': int(round(result['c'] * 100)),
                        })
            elif len(aggregate) == 1:
                quotes_data = polygon_service.get_stock_quotes(stock_data['stock_ticker'], missing_date)
                if result := quotes_data['results'][0] if 'results' in quotes_data and len(quotes_data['results']) else None:
                    daily_prices.append({
                        'stock_id': stock_data['stock_id'],
                        'event_date': missing_date,
                        'price': int(round(result['bid_price'] * 100))
                    })

        stock_dao.update_daily_prices_for_ticker(daily_prices)
        logger.info(f'{len(daily_prices)} daily updates were added for {stock_data["stock_ticker"]}')

    return 'Stock Daily Price update has completed successfully'
