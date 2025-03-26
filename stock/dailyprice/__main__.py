from lib.common.logger import Logger
from lib.services import polygon
from lib.dao import stock
from datetime import datetime, timedelta
from functools import reduce

logger = Logger('stock.dailyprice')

def from_timestamp_to_iso(timestamp):
    return datetime.fromtimestamp(int(round(timestamp / 1000))).date().isoformat()

def main():
    logger.info(f'Function invocation started...')

    stock_dao = stock.StockDao()
    stocks_by_earliest_date = stock_dao.get_stocks_by_earliest_date()
    for stock_data in stocks_by_earliest_date:
        earliest_date = stock_data['earliest_event_date'].date()
        target_date = datetime.date(datetime.now())
        current_date = earliest_date

        existing_price_dates = stock_dao.get_daily_prices_by_dates(stock_data['stock_ticker'], earliest_date, target_date)

        polygon_service = polygon.PolygonService()
        historical_prices = polygon_service.get_stock_historical_data(stock_data['stock_ticker'], earliest_date, target_date)

        date_key = 'stock_price_event_date'
        price_key = 'stock_daily_price'
        existing_prices_by_dates = reduce(
            lambda mapping, price: {**mapping, price[date_key].isoformat(): price[price_key]},
            existing_price_dates,
            {}
        )
        historical_prices_by_dates = reduce(
            lambda mapping, price: {**mapping, from_timestamp_to_iso(price['t']): int(round(price['c'] * 100))},
            historical_prices['results'],
            {}
        )

        daily_prices = []
        current_price = None
        while current_date < target_date:
            iso_format_key = current_date.isoformat()
            if iso_format_key in existing_prices_by_dates:
                current_price = existing_prices_by_dates[iso_format_key]
            elif iso_format_key in historical_prices_by_dates:
                daily_prices.append({
                    'stock_id': stock_data['stock_id'],
                    'event_date': iso_format_key,
                    'price': historical_prices_by_dates[iso_format_key]
                })
            elif current_price:
                daily_prices.append({
                    'stock_id': stock_data['stock_id'],
                    'event_date': iso_format_key,
                    'price': current_price
                })
            current_date += timedelta(days=1)

        stock_dao.update_daily_prices_for_ticker(daily_prices)
        logger.info(f'{len(daily_prices)} daily updates were added for {stock_data["stock_ticker"]}')

    return {'body': 'Stock Daily Price update has completed successfully', 'statusCode': 200}
