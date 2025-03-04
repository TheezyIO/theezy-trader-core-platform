from lib.common.logger import Logger
from lib.common.utils import validate_fields
from lib.security import authorization
from lib.services import portfolio

logger = Logger('portfolio.follower')

field_validation_list = [('id', str)]

def main(args):
    logger.info(f'Function invocation started...')

    authorized_user = authorization.verify_header(args)
    if not authorized_user:
        return {'statusCode': 401, 'body': { 'message': 'Unauthorized'}}

    if not validate_fields(field_validation_list, args):
        return {'statusCode': 400, 'body': { 'message': 'Missing or invalid parameters'}}

    portfolio_service = portfolio.PortfolioService(args['http']['headers']['authorization'])
    if args['http']['method'] == 'PUT':
        response = portfolio_service.follow_portfolio(args['id'])
    elif args['http']['method'] == 'DELETE':
        response = portfolio_service.unfollow_portfolio(args['id'])
    else:
        return {'statusCode': 405, 'body': { 'message': 'Method not allowed'}}

    return {'statusCode': 200, 'body': response}
