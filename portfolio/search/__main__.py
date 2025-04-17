from lib.common.logger import Logger
from lib.dao import portfolio
from lib.security import authorization

logger = Logger(f'portfolio.search')

def main(args):
    logger.info(f'Function invocation started...')

    authorized_user = authorization.verify_header(args)

    if not authorized_user:
        return {'body': {'message': 'Unauthorized'}, 'statusCode': 401}

    if args['http']['method'] != 'GET':
        return {'statusCode': 405, 'body': { 'message': 'Method not allowed'}}

    portfolio_dao = portfolio.PortfolioDao()
    portfolios = portfolio_dao.get_portfolios_for_user(authorized_user['sub'])
    return {
        'statusCode': 200,
        'body': list(map(
            lambda p: {
                'id': p['id'],
                'name': p['portfolio_name'],
                'description': p['portfolio_description'],
                'isFollowing': True if p['portfolio_follower_user_id'] else False,
                'isMember': True if p['portfolio_member_user_id'] else False,
                'minimumDeposit': p['portfolio_minimum_deposit'],
                'maxMembers': p['portfolio_max_members'],
                'members': p['portfolio_members'],
                'followers': p['portfolio_followers'],
                'ownerName': p['portfolio_owner_name'],
                'changeIn7Days': p['portfolio_change_7d'],
                'changeIn30Days': p['portfolio_change_30d'],
                'changeIn365Days': p['portfolio_change_365d'],
                'createdAt': str(p['portfolio_created_at'])
            },
            portfolios
        ))
    }


if __name__ == '__main__':
    print(main({}))
