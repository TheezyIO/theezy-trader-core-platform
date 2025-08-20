from lib.common.logger import Logger
from lib.security import authorization
from lib.dao import portfolio
from lib.common.utils import validate_all_fields

logger = Logger('portfolio.delete')

field_validation_list = [('id', str)]


def main(args):
    logger.info(f'Function invocation started...')

    authorized_user = authorization.verify_header(args)
    if not authorized_user:
        return {'statusCode': 401, 'body': {'message': 'Unauthorized'}}

    if args['http']['method'] != 'DELETE':
        return {'statusCode': 405, 'body': {'message': 'Method not allowed'}}

    if not validate_all_fields(field_validation_list, args):
        return {'statusCode': 400, 'body': {'message': 'Missing or invalid parameters'}}

    portfolio_dao = portfolio.PortfolioDao()
    portfolio_record = portfolio_dao.get_portfolio_by_id(args['id'], authorized_user['sub'])

    if not portfolio_record:
        return {
            'statusCode': 404,
            'body': {'message': 'Portfolio not found', 'status': 'failed'}
        }

    if authorized_user['sub'] != portfolio_record['portfolio_owner_id']:
        return {
            'statusCode': 403,
            'body': {
                'message': 'Unable to delete portfolio - user unauthorized',
                'status': 'failed'
            }
        }

    if portfolio_record['portfolio_cash_balance'] != 0 or portfolio_record[
        'portfolio_equity_balance'] != 0:
        return {
            'statusCode': 403,
            'body': {
                'message': 'Unable to delete portfolio with cash or equity assets',
                'status': 'failed'
            }
        }

    portfolio_dao.delete_portfolio(args['id'])

    return {
        'statusCode': 200,
        'body': {
            'message': 'Portfolio deleted successfully',
            'status': 'success'
        }
    }