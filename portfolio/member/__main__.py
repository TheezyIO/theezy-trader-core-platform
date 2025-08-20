from lib.common.logger import Logger
from lib.security import authorization
from lib.common.utils import validate_all_fields
from lib.dao import portfolio

logger = Logger('portfolio.member')

field_validation_list = [('portfolioId', str)]

def main(args):
    logger.info(f'Function invocation started...')

    authorized_user = authorization.verify_header(args)
    if not authorized_user:
        return {'statusCode': 401, 'body': { 'message': 'Unauthorized'}}

    if args['http']['method'] != 'GET':
        return {'statusCode': 405, 'body': { 'message': 'Method not allowed'}}

    if not validate_all_fields(field_validation_list, args):
        return {'statusCode': 400, 'body': { 'message': 'Missing or invalid parameters'}}

    portfolio_dao = portfolio.PortfolioDao()
    portfolio_members = portfolio_dao.get_portfolio_members(args['portfolioId'])

    return {
        'statusCode': 200,
        'body': list(
            map(
                lambda member: {
                    'id': member['user_id'],
                    'name': member['user_name'],
                    'contributions': member['portfolio_balance_transaction_amount'],
                    'earnings': 0,
                    'joinedAt': member['portfolio_member_created_at']
                },
                portfolio_members
            )
        )
    }
