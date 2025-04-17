from lib.common.logger import Logger
from lib.common.utils import validate_all_fields
from lib.dao import portfolio
from lib.security import authorization

logger = Logger('portfolio.follower')

field_validation_list = [('id', int)]

def main(args):
    logger.info(f'Function invocation started...')

    authorized_user = authorization.verify_header(args)
    if not authorized_user:
        return {'statusCode': 401, 'body': { 'message': 'Unauthorized'}}

    if not validate_all_fields(field_validation_list, args):
        return {'statusCode': 400, 'body': { 'message': 'Missing or invalid parameters'}}

    portfolio_dao = portfolio.PortfolioDao()
    portfolio_record = portfolio_dao.get_portfolio_by_id(args['id'], authorized_user['sub'])

    if not portfolio_record:
        return {'statusCode': 404, 'body': { 'message': 'Portfolio not found', 'status': 'failed' }}

    is_following = portfolio_record['portfolio_follower_user_id'] == authorized_user['sub']

    if args['http']['method'] == 'PUT':
        if is_following:
            return {'statusCode': 400, 'body': { 'message': 'Portfolio already followed', 'status': 'failed' }}
        else:
            portfolio_dao.follow_portfolio(args['id'], authorized_user['sub'])

    elif args['http']['method'] == 'DELETE':
        if is_following:
            portfolio_dao.unfollow_portfolio(args['id'], authorized_user['sub'])
        else:
            return {'statusCode': 400, 'body': { 'message': 'Portfolio not followed', 'status': 'failed' }}
    else:
        return {'statusCode': 405, 'body': { 'message': 'Method not allowed'}}

    return {
        'statusCode': 200,
        'body': {
            'message': 'Portfolio followed successfully' if not is_following else 'Portfolio unfollowed successfully',
            'status': 'success'
        }
    }
