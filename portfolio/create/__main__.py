from lib.common.logger import Logger
from lib.security import authorization
from lib.services import portfolio
from lib.common.utils import validate_all_fields

logger = Logger('portfolio.create')

field_validation_list = [
    ('name', str),
    ('description', str),
    ('minimumDeposit', int),
    ('maxMembers', int)
]

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
        'name': args['name'],
        'description': args['description'],
        'minimumDeposit': args['minimumDeposit'],
        'maxMembers': args['maxMembers']
    }
    logger.info(f'Creating portfolio... {request_body}')

    portfolio_service = portfolio.PortfolioService(args['http']['headers']['authorization'])
    response = portfolio_service.create_portfolio(request_body)

    return portfolio_service.send_response(response)
