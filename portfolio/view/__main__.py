from lib.common.logger import Logger
from lib.security import authorization
from lib.services import portfolio

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

    portfolio_service = portfolio.PortfolioService(args['http']['headers']['authorization'])
    response = portfolio_service.get_portfolio(args['id'])
    return {'statusCode': 200, 'body': response }


if __name__ == '__main__':
    print(main({'message':'Testing newrelic logging'}))
