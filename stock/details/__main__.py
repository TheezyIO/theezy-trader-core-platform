from lib.common.utils import validate_all_fields
from lib.common.logger import Logger
from lib.common import constants
from lib.security import authorization
from lib.services import polygon
from lib.dao import stock
from datetime import datetime

field_validation_list = [
    ('portfolioId', str),
    ('ticker', str)
]

logger = Logger('stock.details')

def get_timespan(difference):
    multiplier = 6
    if difference > constants.time.millis_in_month * multiplier:
        return 'month'
    if difference > constants.time.millis_in_week * multiplier:
        return 'week'
    if difference > constants.time.millis_in_day * multiplier:
        return 'day'
    if difference > constants.time.millis_in_hour * multiplier:
        return 'hour'
    return 'minute'

def main(args):
    logger.info(f'Function invocation started...')

    authorized_user = authorization.verify_header(args)

    if not authorized_user:
        return {'statusCode': 401, 'body': { 'message': 'Unauthorized'}}

    if args['http']['method'] != 'GET':
        return {'statusCode': 405, 'body': { 'message': 'Method not allowed'}}

    if not validate_all_fields(field_validation_list, args):
        return {'statusCode': 400, 'body': { 'message': 'Missing required field parameters'}}

    stock_dao = stock.StockDao()
    portfolio_stock_response = stock_dao.get_portfolio_stock_details(args['portfolioId'], args['ticker'], authorized_user['sub'])

    if not portfolio_stock_response:
        return {
            'statusCode': 404,
            'body': {
                'status': 'failed',
                'message': 'This portfolio does not exist'
            }
        }

    [stock_details] = portfolio_stock_response
    if not stock_details['portfolio_stock_id']:
        return {
            'statusCode': 404,
            'body': {
                'status': 'failed',
                'message': f'The stock {args["ticker"]} does not exist in this portfolio'
            }
        }

    polygon_service = polygon.PolygonService()
    current_datetime = datetime.now()
    start_timestamp = round(stock_details['portfolio_stock_created_at'].timestamp() * 1000)
    current_timestamp = round(current_datetime.timestamp() * 1000)
    difference = current_timestamp - start_timestamp

    timespan = get_timespan(difference)
    stock_data = polygon_service.get_stock_historical_data(args['ticker'], start_timestamp, current_timestamp, timespan)
    portfolio_balance = stock_details['portfolio_cash_balance'] + stock_details['portfolio_equity_balance']
    price_chart = list(
        map(
            lambda result: {
                'close': round(result['c'] * 100),
                'open': round(result['o'] * 100),
                'timestamp': result['t'],
                'volume': result['v']
            },
            stock_data['results']
        )
    ) if stock_data.get('resultsCount') else []
    return {
        'statusCode': 200,
        'body': {
            'id': stock_details['portfolio_stock_id'],
            'priceChart': price_chart,
            'ticker': args['ticker'],
            'name': stock_details['stock_name'],
            'timestamp': stock_details['portfolio_stock_created_at'].isoformat(),
            'averageCost': stock_details['portfolio_stock_average_price'],
            'amount': stock_details['portfolio_stock_amount'],
            'portfolioBalance': portfolio_balance,
            'isPortfolioOwner': stock_details['user_id'] == authorized_user['sub']
        }
    }
