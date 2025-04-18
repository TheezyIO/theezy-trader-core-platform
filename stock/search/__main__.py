from functools import reduce
from urllib.parse import urlparse, parse_qs
from lib.common.logger import Logger
from lib.security import authorization
from lib.services import polygon
from lib.dao import stock
from lib.common.utils import validate_any_field

field_validation_list = [
    ('portfolioId', str),
    ('search', str),
    ('cursor', str)
]

logger = Logger('stock.search')

def valid_stat_field(snapshot, stat_field):
    return stat_field[0] in snapshot and stat_field[1] in snapshot[stat_field[0]] and snapshot[stat_field[0]][stat_field[1]] > 0

def create_stock_with_snapshot(snapshot, stocks_by_ticker, stat_fields):
    (field, key) = reduce(lambda current_f_k, target_f_k: target_f_k if valid_stat_field(snapshot, target_f_k) else current_f_k, stat_fields, stat_fields[0])
    stock_record = stocks_by_ticker[snapshot['ticker']]
    return {
        'ticker': snapshot['ticker'],
        'name': stock_record['name'],
        'price': round(snapshot[field][key] * 100)
    }

def main(args):
    logger.info(f'Function invocation started...')

    authorized_user = authorization.verify_header(args)

    if not authorized_user:
        return {'statusCode': 401, 'body': { 'message': 'Unauthorized'}}

    if args['http']['method'] != 'GET':
        return {'statusCode': 405, 'body': { 'message': 'Method not allowed'}}

    if not validate_any_field(field_validation_list, args):
        return {'statusCode': 400, 'body': { 'message': 'Missing field parameters'}}

    stock_dao = stock.StockDao()
    if 'portfolioId' in args:
        stocks = stock_dao.get_stocks_in_portfolio(args['portfolioId'])
        return {
            'statusCode': 200,
            'body': list(
                map(lambda s: {
                    'id': s['portfolio_stock_id'],
                    'ticker': s['stock_ticker'],
                    'name': s['stock_name'],
                    'price': s['portfolio_stock_average_price'],
                    'amount': s['portfolio_stock_amount']
                }, stocks)
            )
        }
    else:
        polygon_service = polygon.PolygonService()
        stocks_response = polygon_service.search_stocks(args.get('search'), cursor=args.get('cursor'))
        snapshots_response = polygon_service.get_stock_snapshots(list(map(lambda s: s['ticker'], stocks_response['results'])))
        stocks_by_ticker = {s['ticker']: s for s in stocks_response['results']}

        default_stat_field = ('lastQuote', 'P')
        stat_fields = [default_stat_field, ('lastTrade', 'p'), ('prevDay', 'c')]
        parsed_url = urlparse(stocks_response['next_url'])
        parsed_query_params = parse_qs(parsed_url.query)

        stocks = list(
            map(
                lambda snapshot: create_stock_with_snapshot(snapshot, stocks_by_ticker, stat_fields),
                snapshots_response['tickers']
            )
        )

        return {
            'statusCode': 200,
            'body': {
                'cursor': parsed_query_params['cursor'][0] if 'cursor' in parsed_query_params else None,
                'results': list(
                    map(
                        lambda s: {
                            'ticker': s['ticker'],
                            'name': s['name'],
                            'price': s['price']
                        },
                        stocks
                    )
                )
            }
        }
