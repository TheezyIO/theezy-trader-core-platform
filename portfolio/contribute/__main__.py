from lib.common.logger import Logger
from lib.security import authorization
from lib.services import portfolio
from lib.common.utils import validate_fields

logger = Logger('portfolio.contribute')

field_validation_list = [
    ('portfolioId', str),
    ('amount', int)
]

def main(args):
    logger.info(f'Function invocation started...')

    authorized_user = authorization.verify_header(args)
    if not authorized_user:
        return {'statusCode': 401, 'body': { 'message': 'Unauthorized'}}

    if args['http']['method'] != 'POST':
        return {'statusCode': 405, 'body': { 'message': 'Method not allowed'}}

    if not validate_fields(field_validation_list, args):
        return {'statusCode': 400, 'body': { 'message': 'Missing or invalid parameters'}}

    request_body = {
        'portfolioId': args['portfolioId'],
        'amount': args['amount']
    }
    logger.info(f'Contributing to portfolio... {request_body}')

    portfolio_service = portfolio.PortfolioService(args['http']['headers']['authorization'])
    response = portfolio_service.contribute_portfolio(request_body)

    return portfolio_service.send_response(response)
