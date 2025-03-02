from lib.common import constants
from lib.common.logger import Logger
from lib.security import authorization
from lib.services import portfolio

logger = Logger('portfolio.view')

def main(args):
    logger.info(f'Function invoked with the following request {args}')

    authorized_user = authorization.verify_header(args)
    if not authorized_user:
        return {'statusCode': 401, 'body': { 'message': 'Unauthorized'}}

    portfolio_service = portfolio.PortfolioService(args['http']['headers']['authorization'])
    response = portfolio_service.get_portfolio('')
    return {'statusCode': 200, 'body': response }


if __name__ == '__main__':
    print(main({'message':'Testing newrelic logging'}))
