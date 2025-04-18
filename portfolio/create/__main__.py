from lib.common.logger import Logger
from lib.common.utils import validate_all_fields
from lib.security import authorization
from lib.dao import portfolio
from datetime import datetime

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

    if args['minimumDeposit'] < 100:
        return {'statusCode': 400, 'body': { 'message': 'Minimum deposit must be at least $1.00'}}

    if args['maxMembers'] <= 1:
        return {'statusCode': 400, 'body': { 'message': 'Maximum number of members must be at least 2'}}

    request_body = {
        'name': args['name'],
        'description': args['description'],
        'minimum_deposit': args['minimumDeposit'],
        'max_members': args['maxMembers'],
        'user_id': authorized_user['sub'],
        'created_at': datetime.now(),
        'change_7d': 0,
        'change_30d': 0,
        'change_365d': 0,
        'followers': 0,
        'members': 0
    }

    portfolio_dao = portfolio.PortfolioDao()
    portfolio_dao.create_portfolio(request_body)

    return {
        'statusCode': 200,
        'body': {
            'message': 'Portfolio created successfully',
            'status': 'success'
        }
    }
