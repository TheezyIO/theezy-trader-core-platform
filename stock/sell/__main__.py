from lib.common.logger import Logger
from lib.security import authorization
from lib.services import stock
from lib.common.utils import validate_all_fields

field_validation_list = [
    ('amount', int),
    ('portfolioId', str),
    ('stock', dict)
]

logger = Logger('stock.sell')

def main(args):
    logger.info(f'Function invocation started...')

    authorized_user = authorization.verify_header(args)
    if not authorized_user:
        return {'statusCode': 401, 'body': { 'message': 'Unauthorized'}}

    if args['http']['method'] != 'POST':
        return {'statusCode': 405, 'body': { 'message': 'Method not allowed'}}

    if not validate_all_fields(field_validation_list, args):
        return {'statusCode': 400, 'body': { 'message': 'Missing or invalid parameters'}}

    request_body = {
        'amount': args['amount'],
        'portfolioId': args['portfolioId'],
        'stock': args['stock']
    }
    stock_service = stock.StockService(args['http']['headers']['authorization'])
    response = stock_service.sell(request_body)

    return stock_service.send_response(response)
