from lib.common.logger import Logger
from lib.security import authorization
from lib.services import portfolio


logger = Logger(f'portfolio.search')

def main(args):
    http_request = args.get('http')
    logger.info(f'Function invoked with the following request {http_request}')

    authorized_user = authorization.verify_header(args)

    if not authorized_user:
        return {'body': {'message': 'Unauthorized'}, 'statusCode': 401}

    portfolio_service = portfolio.PortfolioService(args['http']['headers']['authorization'])
    response = portfolio_service.get_portfolios()
    return {'body': response, 'statusCode': 200 }


if __name__ == '__main__':
    print(main({}))
