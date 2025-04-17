from lib.common.logger import Logger
from lib.security import authorization
from lib.common.utils import validate_all_fields
from lib.dao import portfolio

logger = Logger('portfolio.update')

field_validation_list = [
    ('id', int),
    ('name', str),
    ('description', str),
    ('maxMembers', int)
]

def main(args):
    logger.info(f'Function invocation started...')

    authorized_user = authorization.verify_header(args)
    if not authorized_user:
        return {'statusCode': 401, 'body': { 'message': 'Unauthorized'}}

    if args['http']['method'] != 'PUT':
        return {'statusCode': 405, 'body': { 'message': 'Method not allowed'}}

    if not validate_all_fields(field_validation_list, args):
        return {'statusCode': 400, 'body': { 'message': 'Missing or invalid parameters'}}

    if args['maxMembers'] <= 1:
        return {'statusCode': 400, 'body': { 'message': 'Maximum number of members must be at least 2'}}

    request_body = {
        'name': args['name'],
        'description': args['description'],
        'max_members': args['maxMembers']
    }

    portfolio_dao = portfolio.PortfolioDao()
    portfolio_record = portfolio_dao.get_portfolio_by_id(args['id'], authorized_user['sub'])
    if not portfolio_record:
        return {
            'statusCode': 404,
            'body': {
                'status': 'failed',
                'message': 'Portfolio not found'
            }
        }

    if portfolio_record['portfolio_owner_id'] != authorized_user['sub']:
        return {
            'statusCode': 403,
            'body': {
                'status': 'failed',
                'message': 'You are not authorized to update this portfolio'
            }
        }

    if portfolio_record['portfolio_members'] > args['maxMembers']:
        return {
            'statusCode': 400,
            'body': {
                'status': 'failed',
                'message': 'Cannot reduce maximum number of members to below current number of members.'
            }
        }

    logger.info(f'Updating portfolio... {request_body}')
    portfolio_dao.update_portfolio(request_body, args['id'])

    return {
        'statusCode': 200,
        'body': {
            'status': 'success',
            'message': 'Portfolio updated successfully'
        }
    }
