from lib.common.logger import Logger
from lib.security import authorization
from lib.dao import stock


logger = Logger('stock.transaction')

def main(args):
    logger.info(f'Function invocation started...')

    authorized_user = authorization.verify_header(args)

    if not authorized_user:
        return {'statusCode': 401, 'body': { 'message': 'Unauthorized'}}

    if args['http']['method'] != 'GET':
        return {'statusCode': 405, 'body': { 'message': 'Method not allowed'}}

    if not 'id' in args:
        return {'statusCode': 400, 'body': { 'message': 'Missing transaction id'}}

    stock_dao = stock.StockDao()
    transactions = stock_dao.get_portfolio_stock_transactions(args['id'])

    return {
        'statusCode': 200,
        'body': list(
            map(
                lambda t: {
                    'id': t['stock_id'],
                    'timestamp': t['portfolio_stock_transaction_event_time'].isoformat(),
                    'type': t['transaction_type_name'],
                    'amount': t['portfolio_stock_transaction_amount'],
                    'price': t['portfolio_stock_transaction_price']
                },
                transactions
            )
        )
    }
