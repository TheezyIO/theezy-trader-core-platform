from lib.common.logger import Logger
from lib.security import authorization
from lib.services import stock
from lib.common.utils import validate_any_field

field_validation_list = [
    ('portfolioId', str),
    ('search', str),
    ('cursor', str)
]

logger = Logger('stock.search')

def main(args):
    logger.info(f'Function invocation started...')

    authorized_user = authorization.verify_header(args)

    if not authorized_user:
        return {'statusCode': 401, 'body': { 'message': 'Unauthorized'}}

    if args['http']['method'] != 'GET':
        return {'statusCode': 405, 'body': { 'message': 'Method not allowed'}}

    if not validate_any_field(field_validation_list, args):
        return {'statusCode': 400, 'body': { 'message': 'Missing field parameters'}}

    stock_service = stock.StockService(args['http']['headers']['authorization'])
    response = stock_service.search(args['portfolioId'])

    return stock_service.send_response(response)
