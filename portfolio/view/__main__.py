from lib.common.logger import Logger
from lib.security import authorization
from lib.dao import portfolio

logger = Logger('portfolio.view')

def main(args):
    logger.info(f'Function invocation started...')

    authorized_user = authorization.verify_header(args)
    if not authorized_user:
        return {'statusCode': 401, 'body': { 'message': 'Unauthorized'}}

    if args['http']['method'] != 'GET':
        return {'statusCode': 405, 'body': { 'message': 'Method not allowed'}}

    if 'id' not in args:
        return {'statusCode': 400, 'body': { 'message': 'Missing portfolio id'}}

    portfolio_dao = portfolio.PortfolioDao()
    response = portfolio_dao.get_portfolio_by_id(args['id'], authorized_user['sub'])
    record = response[0] if response else None
    return {
        'statusCode': 200,
        'body': {
            'id': record['id'],
            'name': record['portfolio_name'],
            'description': record['portfolio_description'],
            'maxMembers': record['portfolio_max_members'],
            'members': record['portfolio_members'],
            'followers': record['portfolio_followers'],
            'ownerName': record['portfolio_owner_name'],
            'totalStocks': record['portfolio_total_stocks'],
            'createdAt': record['portfolio_created_at'],
            'equityBalance': record['portfolio_equity_balance'],
            'cashBalance': record['portfolio_cash_balance'],
            'isFollowing': True if record['portfolio_follower_user_id'] else False,
            'isMember': True if record['portfolio_member_user_id'] else False,
            'isOwner': record['portfolio_owner_id'] == authorized_user['sub'],
            'minimumDeposit': record['portfolio_minimum_deposit'],
            'changeIn7Days': record['portfolio_change_7d'],
            'changeIn30Days': record['portfolio_change_30d'],
            'changeIn365Days': record['portfolio_change_365d']
        }
    } if record else {'statusCode': 404, 'body': { 'message': 'Portfolio not found'}}


if __name__ == '__main__':
    print(main({'message':'Testing newrelic logging'}))
