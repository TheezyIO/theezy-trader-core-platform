from lib.common.logger import Logger
from lib.security import authorization
from lib.services import stock


logger = Logger('stock.search')

def main(args):
    logger.info(f'Function invocation started...')

    authorized_user = authorization.verify_header(args)

    if not authorized_user:
        return {'statusCode': 401, 'body': { 'message': 'Unauthorized'}}

    if args['http']['method'] != 'GET':
        return {'statusCode': 405, 'body': { 'message': 'Method not allowed'}}

    if 'portfolioId' not in args:
        return {'statusCode': 400, 'body': { 'message': 'Missing portfolio id'}}

    stock_service = stock.StockService(args['http']['headers']['authorization'])
    response = stock_service.search(args['portfolioId'])

    return stock_service.send_response(response)
