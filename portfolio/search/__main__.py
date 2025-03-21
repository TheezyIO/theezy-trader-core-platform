from lib.common.logger import Logger
from lib.security import authorization
from lib.services import portfolio

import lib.dao

logger = Logger(f'portfolio.search')

def main(args):
    logger.info(f'Function invocation started...')

    authorized_user = authorization.verify_header(args)

    if not authorized_user:
        return {'body': {'message': 'Unauthorized'}, 'statusCode': 401}

    if args['http']['method'] != 'GET':
        return {'statusCode': 405, 'body': { 'message': 'Method not allowed'}}

    portfolio_service = portfolio.PortfolioService(args['http']['headers']['authorization'])
    response = portfolio_service.get_portfolios()
    return portfolio_service.send_response(response)


if __name__ == '__main__':
    print(main({}))
